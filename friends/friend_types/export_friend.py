import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser


class ExportFriend(BaseModel):
    id: Optional[UUID]
    user1: ExportUser
    user2: ExportUser
    created_at: datetime.datetime

    def __init__(self, **kwargs):
        if kwargs["user1"]:
            kwargs["user1"] = ExportUser(**kwargs["user1"].model_to_dict())
        if kwargs["user2"]:
            kwargs["user2"] = ExportUser(**kwargs["user2"].model_to_dict())
        super().__init__(**kwargs)

class ExportFriendList(BaseModel):
    friend_list: typing.List[ExportUser]

    # def __init__(self, **kwargs):
    #     if kwargs["friend_list"]:
            # kwargs["friend_list"] = [friend.user1.id]
        # super().__init__(**kwargs)