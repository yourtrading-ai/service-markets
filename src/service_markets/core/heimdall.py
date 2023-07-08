# Desc: FastAPI Depends plugin for controlling access to API endpoints
# It will raise a 403 if the user is not allowed to access the endpoint.
# For the first request, the Aleph network will be queried to see if the user is allowed to access the endpoint.
from typing import Optional, Annotated

from fastapi import HTTPException
from fastapi_walletauth import WalletAuthDep, WalletAuth
from fastapi_walletauth.core import SignatureChallengeTokenAuth
from starlette.requests import Request

from .model import Permission, Service


class ServicePermissionAuth(SignatureChallengeTokenAuth):
    def __init__(
        self,
        service_url: str,
    ):
        super().__init__()
        self.service_url = service_url

    def __call__(self, request: Request) -> WalletAuth:
        wallet_auth: WalletAuth = super().__call__(request)
        return await check_permission(wallet_auth, self.service_url)


async def check_permission(
    wallet_auth: WalletAuthDep,
    service_url: str,
) -> WalletAuth:
    """
    Check if the user has the given permission for the given service.
    """
    service = await Service.filter(url=service_url).first()
    permission_record = await Permission.filter(
        user_address=wallet_auth.address,
        service_id=service.item_hash,
    ).first()
    if not permission_record:
        raise HTTPException(status_code=403, detail="User does not have permission to access this service")
    return wallet_auth
