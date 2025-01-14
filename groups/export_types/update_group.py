from typing import Optional

from pydantic import BaseModel


class UpdateGroupRequestType(BaseModel):
    group_id: str
    name: Optional[str] = None
    image: Optional[str] = None
