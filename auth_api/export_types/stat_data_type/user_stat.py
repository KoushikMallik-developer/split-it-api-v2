from uuid import UUID

from _decimal import Decimal
from pydantic import BaseModel
from datetime import datetime
from typing import List


class GroupBalanceModel(BaseModel):
    group_id: UUID
    group_name: str
    total_spent: Decimal


class ExpenseModel(BaseModel):
    id: UUID
    amount: Decimal
    created_at: datetime


class UserStatModel(BaseModel):
    friends_count: int
    groups_count: int
    transaction_count: int
    total_balance: Decimal
    payable: Decimal
    receivable: Decimal
    account_created_at: datetime
    group_balance: List[GroupBalanceModel]
    recent_transactions: List[ExpenseModel]
