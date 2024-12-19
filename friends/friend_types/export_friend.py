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
        if isinstance(kwargs["user1"], User):
            kwargs["user1"] = ExportUser(**kwargs["user1"].model_to_dict())
        if isinstance(kwargs["user2"], User):
            kwargs["user2"] = ExportUser(**kwargs["user2"].model_to_dict())
        super().__init__(**kwargs)


class ExportFriendList(BaseModel):
    friend_list: typing.List[ExportUser]

    def __init__(self, user_id: str, **kwargs):
        """

        These file is designed to transform and export friendship data from Django models (User) into
        API-ready formats (ExportUser), ensuring clean and consistent data for frontend or external systems.

        user1: The first user in the friendship, represented by ExportUser.
        user2: The second user in the friendship, represented by ExportUser.

        friend_list: A list of ExportUser objects.

        friend_list contains only the friends of the user with user_id, excluding the user themselves.

        The purpose of this code is to filter out the current user (user_id) from the friend_list. For each friend object:

        If user1 is not the current user, it adds user1 to the new list.
        Otherwise, it adds user2 to the new list.

        """

        if kwargs["friend_list"]:
            kwargs["friend_list"] = [
                friend.user1 if friend.user1.id != uuid.UUID(user_id) else friend.user2
                for friend in kwargs["friend_list"]
            ]
        super().__init__(**kwargs)
