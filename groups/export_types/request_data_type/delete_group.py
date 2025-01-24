from pydantic import BaseModel


class DeleteGroupRequestType(BaseModel):
    group_id: str
