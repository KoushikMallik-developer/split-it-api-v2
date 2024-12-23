from pydantic import BaseModel


class AcceptFriendRequestType(BaseModel):
    user_email: str
