from pydantic import BaseModel


class RemoveFriendRequestType(BaseModel):
    user_email: str
