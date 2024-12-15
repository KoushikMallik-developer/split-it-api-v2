import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ExportFriend(BaseModel):
    # id: Optional[UUID]
    # username: str
    # email: str
    # fname: str
    # lname: str
    # phone: Optional[str]
    # image: Optional[str]
    # is_active: bool
    user1: str
    user2: str
    # created_at: datetime.datetime
    # updated_at: datetime.datetime

    def __init__(self, with_id: bool = True, **kwargs):
        # if not with_id:
        #     kwargs["id"] = None
        super().__init__(**kwargs)


class ExportFriendList(BaseModel):
    friend_list: typing.List[ExportFriend]