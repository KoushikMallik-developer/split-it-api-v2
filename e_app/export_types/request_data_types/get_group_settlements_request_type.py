from pydantic import BaseModel


class GetGroupSettlementsRequestType(BaseModel):
    group_id: str
