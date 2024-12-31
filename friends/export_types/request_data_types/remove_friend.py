from pydantic import BaseModel


class RemoveFriendType(BaseModel):
    user_email: str
