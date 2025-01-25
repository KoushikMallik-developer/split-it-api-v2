from typing import List

from _decimal import Decimal
from pydantic import BaseModel


class AddExpenseRequestType(BaseModel):
    name: str
    group_id: str
    amount: Decimal
    paid_by: str
    participants: List[str]
    category: str
