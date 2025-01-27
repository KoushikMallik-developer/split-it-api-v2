from pydantic import BaseModel


class RemoveFriendRequestType(BaseModel):
    user_id: str
