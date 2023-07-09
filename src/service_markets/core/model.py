from enum import Enum
from typing import List, Optional

from aars import Record
from pydantic import Field


class UserInfo(Record):
    username: str
    address: str
    bio: Optional[str]
    email: Optional[str]
    link: Optional[str]


class Votable(Record):
    upvotes: int = 0
    downvotes: int = 0


class Service(Votable):
    name: str
    description: str
    url: str
    image_url: Optional[str]
    price: float
    tags: List[str]
    owner_address: str
    comment_counter: int = 0
    payment_id: Optional[str] = None


class VoteType(str, Enum):
    UP = "up"
    DOWN = "down"


class VotableType(str, Enum):
    SERVICE = "service"
    COMMENT = "comment"


class Vote(Record):
    item_id: str
    item_type: VotableType
    user_address: str
    vote: VoteType


class Comment(Votable):
    service_id: str
    user_address: str
    comment: str


class Permission(Record):
    user_address: str
    service_id: str


class Payment(Record):
    contractAddress: str
    tokenAddress: str
    txHash: str
    to: str
    from_: str = Field(alias="from")
    amount: str
    reference: str
