from pydantic import BaseModel


class RemoveExpenseRequestType(BaseModel):
    expense_id: str
