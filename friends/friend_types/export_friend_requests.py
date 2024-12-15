import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ExportFriendRequest(BaseModel):
    # id: Optional[UUID]
    # username: str
    # email: str
    # fname: str
    # lname: str
    # phone: Optional[str]
    # image: Optional[str]
    # is_active: bool
    sender: str
    receiver: str
    # created_at: datetime.datetime
    # updated_at: datetime.datetime

    def __init__(self, with_id: bool = True, **kwargs):
        # if not with_id:
        #     kwargs["id"] = None
        super().__init__(**kwargs)


class ExportFriendRequestList(BaseModel):
    friend_requests: typing.List[ExportFriendRequest]