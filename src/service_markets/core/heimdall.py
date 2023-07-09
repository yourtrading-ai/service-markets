# Desc: FastAPI Depends plugin for controlling access to API endpoints
# It will raise a 403 if the user is not allowed to access the endpoint.
# For the first request, the Aleph network will be queried to see if the user is allowed to access the endpoint.
import asyncio
from typing import Optional, List

from aars import AARS, Index
from fastapi import HTTPException, FastAPI
from fastapi_walletauth import WalletAuth, authorization_routes
from fastapi_walletauth.core import SignatureChallengeTokenAuth
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .model import Permission, Service
from .session import initialize_aars


Index(Service, "url")
Index(Permission, ["user_address", "service_id"])


class ServicePermissionAuth(SignatureChallengeTokenAuth):
    aars: AARS
    service_record: Optional[Service] = None
    cached_permissions = {}
    ready = False

    def __init__(
        self,
        service_url: str,
    ):
        super().__init__()
        self.service_url = service_url

    def __call__(self, request: Request) -> WalletAuth:
        """
        Check if the user has the given permission for the given service.
        """
        wallet_auth: WalletAuth = super().__call__(request)
        if self.cached_permissions.get(wallet_auth.address):
            return wallet_auth
        loop = self.aars.session.http_session.loop
        permission_record = loop.run_until_complete(
            Permission.filter(
                user_address=wallet_auth.address,
                service_id=self.service_record.item_hash,
            ).all()
        )
        if not permission_record:
            raise HTTPException(
                status_code=403,
                detail="User does not have permission to access this service",
            )
        self.cached_permissions[wallet_auth.address] = permission_record
        return wallet_auth

    async def setup(self, **kwargs):
        self.aars = await initialize_aars(**kwargs)
        print(f"Heimdall re-indexing channel {AARS.channel}")
        await Permission.fetch_objects().all()
        services = await Service.fetch_objects().all()
        service = next(filter(lambda s: s.url == self.service_url, services), None)
        if not service:
            raise ValueError(
                f"Service with url {self.service_url} is not registered on service.markets"
            )
        print(f"Service {self.service_url} successfully loaded. Heimdall is ready.")
        self.service_record = service
        self.ready = True


class HeimdallMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        backend: ServicePermissionAuth,
        open_routes: List[str],
        open_endpoints: List[str],
        **kwargs,
    ):
        super().__init__(app)
        self.backend = backend
        self.open_routes = open_routes
        self.open_endpoints = open_endpoints
        self.kwargs = kwargs

    async def dispatch(self, request, call_next):
        if (
            not any([request.url.path.startswith(route) for route in self.open_routes])
            and not any([not request.url.path == endpoint for endpoint in self.open_endpoints])
        ):
            if not self.backend.ready:
                await self.backend.setup(**self.kwargs)
            request.state.wallet_auth = self.backend(request)
        return await call_next(request)


def setup_heimdall(app: FastAPI, service_url: str, **kwargs):
    """
    Setup Heimdall middleware for the given app. This will check if the user has permission to access the given service.
    Permission is checked by querying the Aleph network.
    """
    if kwargs["open_routes"]:
        open_routes = kwargs["open_routes"]
        del kwargs["open_routes"]
    else:
        open_routes = [
            "/authorization",
            "/docs",
            "/openapi.json",
            "/redoc",
        ]
    if kwargs["open_endpoints"]:
        open_endpoints = kwargs["open_endpoints"]
        del kwargs["open_endpoints"]
    else:
        open_endpoints = [
            "/",
        ]
    app.add_middleware(
        HeimdallMiddleware,
        backend=ServicePermissionAuth(service_url),
        open_routes=open_routes,
        open_endpoints=open_endpoints,
        **kwargs,
    )
    app.include_router(authorization_routes)
