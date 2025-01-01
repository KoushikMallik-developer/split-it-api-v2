from typing import Optional

from pydantic import BaseModel


class SignInRequestType(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
