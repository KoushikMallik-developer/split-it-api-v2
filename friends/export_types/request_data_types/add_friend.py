from pydantic import BaseModel


class AddFriendRequestType(BaseModel):
    user_id: str
