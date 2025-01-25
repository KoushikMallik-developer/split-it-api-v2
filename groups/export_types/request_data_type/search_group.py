from pydantic import BaseModel


class SearchGroupRequestType(BaseModel):
    keyword: str
