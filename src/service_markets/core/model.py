from enum import Enum
from typing import List, Optional

from aars import Record


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
    tags: List[str]
    owner_address: str
    comment_counter: int = 0


class VoteType(Enum):
    UP = 1
    DOWN = -1


class VotableType(Enum):
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
