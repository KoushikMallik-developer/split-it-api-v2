from pydantic import BaseModel


class AddFriendRequestType(BaseModel):
    user_email: str
