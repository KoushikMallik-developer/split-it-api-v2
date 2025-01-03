from typing import Optional, List

from pydantic import BaseModel

from auth_api.models.user_models.user import User


class CreateGroupRequestType(BaseModel):
    members: Optional[List[User]] = None
    name: str
    image: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
