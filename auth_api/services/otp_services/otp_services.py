import base64
from typing import Optional

from django.core.cache import cache
from django.utils import timezone

from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.email_verification import UserEmailVerification
from auth_api.models.user_models.user import User
from auth_api.services.email_services.email_services import EmailServices
from auth_api.services.otp_services.otp_generator import OTPGenerator


class OTPServices:
    def __init__(self):
        self.KEYWORD_PREFIX = "_VERIFICATION_OTP"
        self.expiration_time = 840

    def send_otp_to_user(self, user_email: str) -> Optional[str]:
        email_services = EmailServices()
        cache_keyword = f"{user_email.upper()}{self.KEYWORD_PREFIX}"
        cached_data = cache.get(cache_keyword)
        db_user = User.objects.get(email=user_email)
        if cached_data:
            response = email_services.send_otp_email_by_user_email(
                user_email=user_email, otp=base64.b64decode(cached_data).decode("utf-8")
            )
        else:
            UserEmailVerification.objects.filter(user=db_user).delete()
            verification_data: UserEmailVerification = self.__create_otp(user=db_user)
            cache.set(
                cache_keyword,
                base64.b64encode(verification_data.code.encode("utf-8")),
                self.expiration_time,
            )
            response = email_services.send_otp_email_by_user_email(
                user_email=user_email, otp=verification_data.code
            )

        return response

    def __create_otp(self, user: User) -> UserEmailVerification:
        generator = OTPGenerator()
        code = generator.generate_otp()
        ecom_verification_obj = UserEmailVerification(user=user, code=code)
        ecom_verification_obj.save()
        return ecom_verification_obj

    def __validate_otp(self, user: User, otp) -> bool:
        try:
            ecom_verification_obj = UserEmailVerification.objects.get(
                user=user, code=otp, expiration_time__gte=timezone.now()
            )
            ecom_verification_obj.delete()
            return True
        except Exception:
            return False

    def verify_otp(self, user: ExportUser, otp) -> bool:
        user = User.objects.get(email=user.email)
        if self.__validate_otp(user=user, otp=otp):
            user.is_active = True
            user.save()
            return True
        else:
            return False
