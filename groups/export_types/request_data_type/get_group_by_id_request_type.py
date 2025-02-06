from pydantic import BaseModel


class GetGroupByIdRequestType(BaseModel):
    group_id: str
