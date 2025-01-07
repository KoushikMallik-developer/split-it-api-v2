from typing import Optional, List

from pydantic import BaseModel


class AddMemberRequestType(BaseModel):
    user_email: str
    group_id: str
