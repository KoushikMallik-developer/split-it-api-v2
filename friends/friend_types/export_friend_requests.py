import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser


class ExportFriendRequest(BaseModel):
    id: Optional[UUID]
    sender: ExportUser
    receiver: ExportUser
    created_at: datetime.datetime

    def __init__(self, **kwargs):
        if kwargs["sender"]:
            kwargs["sender"] = ExportUser(**kwargs["sender"].model_to_dict())
        if kwargs["receiver"]:
            kwargs["receiver"] = ExportUser(**kwargs["receiver"].model_to_dict())
        super().__init__(**kwargs)


class ExportFriendRequestList(BaseModel):
    friend_requests: typing.List[ExportFriendRequest]
