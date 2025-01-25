from typing import Optional

from pydantic import BaseModel


class SearchGroupRequestType(BaseModel):
    keyword: str
