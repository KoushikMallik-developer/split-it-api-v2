from __future__ import annotations
from typing import Optional, List

from django.template.loader import render_to_string
from pydantic import BaseModel

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.user import User
from auth_api.services.definitions import default_email
from auth_api.services.helpers import validate_user_email


class AuthEmailMessage(BaseModel):
    subject: str
    body: str
    from_email: Optional[str]
    to: List[str]
    bcc: Optional[str] = None
    attachments: Optional[str] = None
    headers: Optional[str] = None
    cc: Optional[str] = None
    reply_to: Optional[str] = None

    @classmethod
    def create_password_reset_email_by_user_email(
        cls, user_email: str, reset_url: str
    ) -> AuthEmailMessage:
        if user_email:
            if validate_user_email(user_email).is_validated:
                user = ExportUser(**User.objects.get(email=user_email).model_to_dict())
                context = {"fname": user.fname, "reset_url": reset_url}
                html_content = render_to_string("password_reset_email.html", context)
                return cls(
                    subject="Split It User Password Reset",
                    body=html_content,
                    from_email=f"Split It <{default_email}>",
                    to=[user_email],
                )
            else:
                raise ValueError
        else:
            raise ValueError

    @classmethod
    def create_otp_html_email_by_user_email(
        cls, user_email: str, otp: str
    ) -> AuthEmailMessage:
        if user_email:
            if User.objects.filter(email=user_email).count() > 0:
                user = ExportUser(**User.objects.get(email=user_email).model_to_dict())
                context = {"fname": user.fname, "otp": otp}
                html_content = render_to_string("otp_email.html", context)
                return cls(
                    subject="Split It User Verification",
                    body=html_content,
                    from_email=f"Split It <{default_email}>",
                    to=[user_email],
                )
            else:
                raise ValueError
        else:
            raise ValueError
