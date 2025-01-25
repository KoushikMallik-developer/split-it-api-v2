import typing
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User


class ExportGroup(BaseModel):
    id: Optional[UUID]
    creator: ExportUser
    name: str
    description: Optional[str]
    members: Optional[List[ExportUser]] = []
    created_at: datetime
    updated_at: datetime

    def __init__(self, **kwargs):
        if "creator" in kwargs and isinstance(kwargs["creator"], User):
            kwargs["creator"] = ExportUser(**kwargs["creator"].model_to_dict())

        if "members" in kwargs and kwargs["members"]:
            kwargs["members"] = [
                ExportUser(**member.model_to_dict()) for member in kwargs["members"]
            ]

        super().__init__(**kwargs)


class ExportGroupList(BaseModel):
    group_list: typing.List[ExportGroup]
