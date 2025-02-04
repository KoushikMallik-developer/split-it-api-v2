from typing import Optional

from pydantic import BaseModel


class GetGroupExpenseRequestType(BaseModel):
    group_id: str
    count: Optional[int] = 0
