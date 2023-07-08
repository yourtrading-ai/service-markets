import asyncio
from typing import List, Optional, TypeVar, Tuple

from fastapi import APIRouter, HTTPException
from fastapi_walletauth import WalletAuthDep

from ...core.model import (
    Service,
    Permission,
    Comment,
    VoteType,
    Vote,
    VotableType,
)
from ..api_model import (
    ServiceWithPermissionStatus,
    UploadServiceRequest,
    VoteServiceResponse,
    VoteCommentResponse,
)

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)

T = TypeVar("T", Service, Comment)


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
                    **service.dict(), permission_status=permission is not None
                )
            )
    else:
        services_response = [
            ServiceWithPermissionStatus(**service.dict(), permission_status=None)
            for service in services
        ]
    return services_response


@router.put("")
async def upload_service(
    service: UploadServiceRequest, wallet: WalletAuthDep
) -> Service:
    """
    Upload a service.
    If an `item_hash` is provided, it will update the service with that id.
    """
    if service.owner_address != wallet.address:
        raise HTTPException(
            status_code=403,
            detail="address does not match currently authorized user wallet",
        )
    if service.item_hash is not None:
        old_service = await Service.fetch(service.item_hash).first()
        if old_service:
            old_service.name = service.name
            old_service.description = service.description
            old_service.owner_address = service.owner_address
            old_service.item_hash = service.item_hash
            old_service.url = service.url
            old_service.image_url = service.image_url
            old_service.tags = service.tags
            old_service.price = service.price
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
            user_address=view_as, service_id=service_id
        ).first()
        return ServiceWithPermissionStatus(
            **service.dict(), permission_status=permission is not None
        )
    return ServiceWithPermissionStatus(**service.dict(), permission_status=None)


@router.get("/{service_id}/permissions")
async def get_service_permissions(service_id: str) -> List[Permission]:
    """
    Get all granted permissions for a given service.
    """
    permissions = await Permission.filter(service_id=service_id).all()
    return permissions


@router.put("/{service_id}/vote")
async def vote_service(
    service_id: str,
    vote: VoteType,
    wallet: WalletAuthDep,
) -> VoteServiceResponse:
    """
    Update your vote for a given service.
    """
    service = await Service.fetch(service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="No Service found")
    vote_record = await Vote.filter(
        item_id=service_id, user_address=wallet.address
    ).first()
    if not vote_record:
        vote_record = Vote(
            item_id=service_id,
            item_type=VotableType.SERVICE.value,
            user_address=wallet.address,
            vote=vote,
        )
    else:
        vote_record.vote = vote
    service, vote_record = await update_vote(service, vote_record)
    return VoteServiceResponse(service=service, vote=vote_record)


@router.get("/{service_id}/comments")
async def get_service_comments(
    service_id: str, page: int = 1, page_size: int = 20
) -> List[Comment]:
    """
    Get all comments for a given service.
    """
    comments = await Comment.filter(service_id=service_id).page(
        page=page, page_size=page_size
    )
    return comments


@router.post("/{service_id}/comments")
async def post_service_comment(
    service_id: str,
    comment: str,
    wallet: WalletAuthDep,
) -> Comment:
    """
    Post a comment for a given service.
    """
    return await Comment(
        service_id=service_id,
        comment=comment,
        user_address=wallet.address,
    ).save()


@router.put("/{service_id}/comments/{comment_id}/vote")
async def vote_service_comment(
    service_id: str,
    comment_id: str,
    vote: VoteType,
    wallet: WalletAuthDep,
) -> VoteCommentResponse:
    """
    Update your vote for a given comment.
    """
    comment = await Comment.fetch(comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="No Comment found")
    vote_record = await Vote.filter(
        item_id=comment_id, user_address=wallet.address
    ).first()
    if not vote_record:
        vote_record = Vote(
            item_id=comment_id,
            item_type=VotableType.COMMENT.value,
            user_address=wallet.address,
            vote=vote,
        )
    else:
        vote_record.vote = vote
    comment, vote_record = await update_vote(comment, vote_record)
    return VoteCommentResponse(comment=comment, vote=vote_record)


async def update_vote(votable: T, vote_record: Vote) -> Tuple[T, Vote]:
    print(vote_record.vote.value, VoteType.UP.value)
    if vote_record.item_hash is not None:
        if vote_record.vote.value == VoteType.UP.value and vote_record.changed:
            votable.downvotes -= 1
            votable.upvotes += 1
        elif vote_record.vote.value == VoteType.DOWN.value and vote_record.changed:
            votable.downvotes += 1
            votable.upvotes -= 1
        await asyncio.gather(
            votable.save(),
            vote_record.save(),
        )
    else:
        votable.upvotes += 1 if vote_record.vote.value == VoteType.UP.value else 0
        votable.downvotes += 1 if vote_record.vote.value == VoteType.DOWN.value else 0
        vote_record, votable = await asyncio.gather(
            vote_record.save(),
            votable.save(),
        )
    return votable, vote_record
