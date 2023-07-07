from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ...core.model import (
    Service,
    Permission, Comment,
)
from ..api_model import (
    ServiceWithPermissionStatus, UploadServiceRequest,
)

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_services(
    view_as: Optional[str] = None,
    by: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> List[ServiceWithPermissionStatus]:
    """
    Get all services or filter by owner address. Use `view_as` to get the permission status for a given user.
    """
    services: List[Service] = []
    if by:
        services = await Service.filter(owner_address=by).page(
            page=page, page_size=page_size
        )
    else:
        services = await Service.fetch_objects().page(page=page, page_size=page_size)

    services_response: List[ServiceWithPermissionStatus] = []
    if view_as:
        permissions = await Permission.filter(user_address=view_as).all()
        for service in services:
            permission = filter(lambda p: p.serviceID == service.item_hash, permissions)
            services_response.append(
                ServiceWithPermissionStatus(
                    service=service,
                    permission_status=permission is not None
                )
            )
    else:
        services_response = [
            ServiceWithPermissionStatus(service=service, permission_status=None)
            for service in services
        ]
    return services_response


@router.put("")
async def upload_service(service: UploadServiceRequest) -> Service:
    """
    Upload a service.
    If an `item_hash` is provided, it will update the service with that id.
    """
    if service.item_hash is not None:
        old_service = await Service.fetch(service.item_hash).first()
        if old_service:
            old_service.name = service.name
            old_service.description = service.description
            old_service.owner_address = service.owner_address
            old_service.item_hash = service.item_hash
            old_service.url = service.url
            old_service.tags = service.tags
        else:
            raise HTTPException(status_code=404, detail="No Service found")
    return await Service(**service.dict()).save()


@router.get("/{service_id}")
async def get_service(
    service_id: str, view_as: Optional[str] = None
) -> ServiceWithPermissionStatus:
    """
    Get a specific service by id.
    """
    service = await Service.fetch(service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="No Service found")
    if view_as:
        permission = await Permission.filter(
            user_address=view_as, serviceID=service_id
        ).first()
        return ServiceWithPermissionStatus(service=service, permission_status=permission is not None)
    return ServiceWithPermissionStatus(service=service, permission_status=None)


@router.get("/{service_id}/permissions")
async def get_service_permissions(service_id: str) -> List[Permission]:
    """
    Get all granted permissions for a given service.
    """
    permissions = await Permission.filter(service_id=service_id).all()
    return permissions


@router.get("/{service_id}/comments")
async def get_service_comments(
    service_id: str,
    page: int = 1,
    page_size: int = 20
) -> List[Comment]:
    """
    Get all comments for a given service.
    """
    comments = await Comment.filter(service_id=service_id).page(
        page=page, page_size=page_size
    )
    return comments
