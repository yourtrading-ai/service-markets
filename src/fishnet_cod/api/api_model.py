from enum import Enum
from typing import List, Optional, Tuple, Union

from aars import Index
from pydantic import BaseModel

from ..core.model import (
    Permission,
    UserInfo,
    Service,
)
from .security import AuthInfo


Index(Service, "owner_address")

Index(Permission, "user_address")
Index(Permission, "service_id")

Index(UserInfo, "address")
Index(UserInfo, "username")


class UploadServiceRequest(BaseModel):
    item_hash: Optional[str]
    name: str
    description: str
    url: str
    owner_address: str
    tags: List[str] = []


class ServiceWithPermissionStatus(Service):
    permitted: Optional[bool] = None


class PutUserInfo(BaseModel):
    username: str
    address: str
    bio: Optional[str]
    email: Optional[str]
    link: Optional[str]


class TokenChallengeResponse(AuthInfo):
    challenge: str


class BearerTokenResponse(AuthInfo):
    token: str


class MessageResponse(BaseModel):
    response: str
