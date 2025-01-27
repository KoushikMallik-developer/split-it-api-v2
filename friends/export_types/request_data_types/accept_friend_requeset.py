from pydantic import BaseModel


class AcceptFriendRequestType(BaseModel):
    user_id: str
