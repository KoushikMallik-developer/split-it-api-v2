from datetime import datetime
from typing import List
from uuid import UUID

from _decimal import Decimal
from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User
from groups.export_types.group_types.export_group import ExportGroup
from groups.models.group import Group


class ExportSettlement(BaseModel):
    id: UUID
    amount: Decimal
    settled_by: ExportUser
    paid_to: ExportUser
    group: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **kwargs):
        if isinstance(kwargs["settled_by"], User):
            kwargs["settled_by"] = ExportUser(**kwargs["settled_by"].model_to_dict())

        if isinstance(kwargs["paid_to"], User):
            kwargs["paid_to"] = ExportUser(**kwargs["paid_to"].model_to_dict())

        if isinstance(kwargs["group"], Group):
            kwargs["group"] = ExportGroup(**kwargs["group"].model_to_dict()).name

        super().__init__(**kwargs)


class ExportSettlementList(BaseModel):
    settlements: List[ExportSettlement]
