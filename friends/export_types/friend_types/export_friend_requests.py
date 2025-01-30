import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User


class ExportFriendRequest(BaseModel):
    """

    These file is designed to transform and export friend request data from Django models (User) into
    API-ready formats (ExportUser), ensuring clean and consistent data for frontend or external systems.

    sender: The user who sent the request, represented by ExportUser.
    receiver: The user who received the request, represented by ExportUser.

    friend_requests: A list of ExportFriendRequest objects.

    friend_requests contains only the friend_requests of the user with user_id along with received and sender.

    """

    id: Optional[UUID]
    user: ExportUser
    created_at: datetime.datetime

    def __init__(self, **kwargs):
        if isinstance(kwargs["receiver"], User):
            kwargs["user"] = ExportUser(**kwargs["receiver"].model_to_dict())
        super().__init__(**kwargs)


class ExportFriendRequestList(BaseModel):
    friend_requests: typing.List[ExportFriendRequest]
