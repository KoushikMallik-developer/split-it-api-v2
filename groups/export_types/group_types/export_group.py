import typing
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from _decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User
from e_app.models.balance import Balance
from groups.group_exceptions.group_exceptions import GroupNotFoundError
from groups.models.group import Group


class ExportGroup(BaseModel):
    id: Optional[UUID]
    creator: ExportUser
    name: str
    description: Optional[str]
    image: Optional[str]
    members: Optional[List[ExportUser]] = []
    total_spent: Optional[Decimal] = None
    created_at: datetime
    balances: Optional[dict]
    updated_at: datetime

    def __init__(self, **kwargs):
        try:
            if "creator" in kwargs and isinstance(kwargs["creator"], User):
                kwargs["creator"] = ExportUser(**kwargs["creator"].model_to_dict())
            members = Group.objects.get(id=kwargs["id"]).members.all()
            kwargs["members"] = [
                ExportUser(**member.model_to_dict()) for member in members
            ]

            balances = Balance.objects.filter(group__id=kwargs["id"])
            kwargs["balances"] = {
                str(balance.user.id): balance.amount for balance in balances
            }

            super().__init__(**kwargs)
        except ObjectDoesNotExist:
            raise GroupNotFoundError()


class ExportGroupList(BaseModel):
    group_list: typing.List[ExportGroup]
