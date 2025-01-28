from _decimal import Decimal
from pydantic import BaseModel


class AddSettlementRequestType(BaseModel):
    group_id: str
    settled_by: str
    paid_to: str
    amount: Decimal
