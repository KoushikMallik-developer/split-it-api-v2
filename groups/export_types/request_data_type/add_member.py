from pydantic import BaseModel


class AddMemberRequestType(BaseModel):
    user_id: str
    group_id: str
