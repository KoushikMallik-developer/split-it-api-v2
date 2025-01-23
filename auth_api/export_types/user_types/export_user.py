from __future__ import annotations
import datetime
import typing
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.models.user_models.user import User


class ExportUser(BaseModel):
    id: Optional[UUID]
    username: str
    email: str
    fname: str
    lname: str
    dob: Optional[datetime.datetime]
    phone: Optional[str]
    image: Optional[str]
    friends: Optional[typing.List[ExportUser]] = []
    expenses: Optional[int] = 0
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __init__(self, with_id: bool = True, with_friends: bool = False, **kwargs):
        if not with_id:
            kwargs["id"] = None
        if not with_friends:
            kwargs["friends"] = []
        else:
            user = User.objects.get(id=kwargs["id"])
            friends = user.friends.all()
            kwargs["friends"] = [
                ExportUser(**friend.model_to_dict()) for friend in friends
            ]
        super().__init__(**kwargs)


class ExportUserList(BaseModel):
    user_list: typing.List[ExportUser]
