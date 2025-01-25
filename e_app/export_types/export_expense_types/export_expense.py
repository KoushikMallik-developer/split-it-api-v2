from datetime import datetime
from typing import List

from _decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User
from e_app.expense_exceptions.expense_exceptions import ExpenseNotFoundError
from e_app.models.expense import Expense
from e_app.models.expense_category import ExpenseCategory
from groups.export_types.group_types.export_group import ExportGroup
from groups.models.group import Group


class ExportExpense(BaseModel):
    name: str
    amount: Decimal
    paid_by: ExportUser
    participants: List[ExportUser]
    category: str
    group: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, **kwargs):
        try:
            if isinstance(kwargs["paid_by"], User):
                kwargs["paid_by"] = ExportUser(**kwargs["paid_by"].model_to_dict())

            participants = Expense.objects.get(id=kwargs["id"]).participants.all()
            kwargs["participants"] = [
                ExportUser(**participant.model_to_dict())
                for participant in participants
            ]

            if isinstance(kwargs["group"], Group):
                kwargs["group"] = ExportGroup(**kwargs["group"].model_to_dict()).name

            if isinstance(kwargs["category"], ExpenseCategory):
                kwargs["category"] = kwargs["category"].name

            super().__init__(**kwargs)

        except ObjectDoesNotExist:
            raise ExpenseNotFoundError()
