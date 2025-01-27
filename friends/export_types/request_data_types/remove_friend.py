from pydantic import BaseModel


class RemoveFriendType(BaseModel):
    user_id: str
