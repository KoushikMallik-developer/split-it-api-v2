from pydantic import BaseModel


class GetGroupExpenseRequestType(BaseModel):
    group_id: str
