from typing import Optional, List

from pydantic import BaseModel


class CreateGroupRequestType(BaseModel):
    members: Optional[List[str]] = None
    name: str
    image: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
