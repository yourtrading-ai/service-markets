from typing import List, Optional

from fastapi import APIRouter, HTTPException

from ..security import WalletAuthDep
from ...core.model import Permission, UserInfo
from ..api_model import PutUserInfo

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def get_users(
    username: Optional[str] = None,
    address: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> List[UserInfo]:
    params = {}
    if username:
        params["username"] = username
    if address:
        params["address"] = address
    if params:
        return await UserInfo.filter(**params).page(page=page, page_size=page_size)
    return await UserInfo.fetch_objects().page(page=page, page_size=page_size)


@router.put("")
async def put_user_info(user_info: PutUserInfo, wallet_auth: WalletAuthDep) -> UserInfo:
    user_record = None
    if user_info.address != wallet_auth.pubkey:
        raise HTTPException(status_code=403, detail="address does not match currently authorized user wallet")
    if user_info.address:
        user_record = await UserInfo.filter(address=user_info.address).first()
        if user_record:
            user_record.username = user_info.username
            user_record.address = user_info.address
            user_record.bio = user_info.bio
            user_record.email = user_info.email
            user_record.link = user_info.link
            await user_record.save()
    if user_record is None:
        user_record = await UserInfo(
            username=user_info.username,
            address=user_info.address,
            bio=user_info.bio,
            email=user_info.email,
            link=user_info.link,
        ).save()
    return user_record


@router.get("/{address}")
async def get_specific_user(address: str) -> Optional[UserInfo]:
    return await UserInfo.filter(address=address).first()


@router.get("/{address}/permissions")
async def get_permissions(
    address: str,
    page: int = 1,
    page_size: int = 20,
) -> List[Permission]:
    permission_records = await Permission.filter(user_address=address).page(
        page=page, page_size=page_size
    )
    return permission_records
