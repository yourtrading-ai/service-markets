from typing import List, Optional

from aars import Index
from pydantic import BaseModel

from ..core.model import (
    Permission,
    UserInfo,
    Service,
    Vote,
    Comment,
    Payment,
)


Index(Service, "owner_address")

Index(Permission, "user_address")
Index(Permission, "service_id")
Index(Permission, ["user_address", "service_id"])

Index(Payment, "txHash")

Index(Comment, "service_id")

Index(Vote, ["item_id", "user_address"])

Index(UserInfo, "address")
Index(UserInfo, "username")


class UploadServiceRequest(BaseModel):
    item_hash: Optional[str]
    name: str
    description: str
    url: str
    image_url: Optional[str]
    price: float
    owner_address: str
    tags: List[str] = []


class ServiceWithPermissionStatus(Service):
    permitted: Optional[bool] = None


class VoteServiceResponse(BaseModel):
    vote: Vote
    service: Service


class PutInvoiceServiceResponse(BaseModel):
    service: Service
    payment: Payment
    permission: Permission


class VoteCommentResponse(BaseModel):
    vote: Vote
    service: Comment


class PutUserInfo(BaseModel):
    username: str
    address: str
    bio: Optional[str]
    email: Optional[str]
    link: Optional[str]


class MessageResponse(BaseModel):
    response: str
