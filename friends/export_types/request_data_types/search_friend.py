from pydantic import BaseModel


class SearchFriendRequestType(BaseModel):
    keyword: str
