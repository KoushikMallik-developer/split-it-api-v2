import datetime
import typing
import uuid
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User


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

    def __init__(self, user_id: str, **kwargs):
        if isinstance(kwargs["friend_list"], User):
            # get friend list except self user from friend list
            kwargs["friend_list"] = [
                friend.user1 if friend.user1.id != uuid.UUID(user_id) else friend.user2
                for friend in kwargs["friend_list"]
            ]
        super().__init__(**kwargs)
