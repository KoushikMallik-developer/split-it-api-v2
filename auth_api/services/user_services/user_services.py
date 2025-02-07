import os
from typing import Optional
from dotenv import load_dotenv
from psycopg2 import DatabaseError

from auth_api.auth_exceptions.user_exceptions import (
    EmailNotSentError,
    UserNotFoundError,
    OTPNotVerifiedError,
    UserAlreadyVerifiedError,
)
from auth_api.export_types.request_data_types.change_password import (
    ChangePasswordRequestType,
)
from auth_api.export_types.request_data_types.create_user import CreateUserRequestType
from auth_api.export_types.request_data_types.sign_in import SignInRequestType
from auth_api.export_types.request_data_types.update_user_profile import (
    UpdateUserProfileRequestType,
)
from auth_api.export_types.request_data_types.verify_otp import VerifyOTPRequestType
from auth_api.export_types.user_types.export_user import ExportUserList, ExportUser
from auth_api.models.user_models.user import User
from auth_api.serializers.user_serializer import UserSerializer
from auth_api.services.definitions import DEFAULT_VERIFICATION_MESSAGE
from auth_api.services.email_services.email_services import EmailServices
from auth_api.services.encryption_services.encryption_service import EncryptionServices
from auth_api.services.helpers import (
    validate_user_email,
    validate_password,
    validate_name,
    string_to_datetime,
    validate_dob,
    validate_phone,
    validate_email_format,
)
from auth_api.services.otp_services.otp_services import OTPServices
from auth_api.services.token_services.token_generator import TokenGenerator


class UserServices:
    @staticmethod
    def get_all_users_service() -> Optional[ExportUserList]:
        try:
            users = User.objects.all()
        except Exception:
            raise DatabaseError()
        if users:
            all_user_details = []
            for user in users:
                user_export_details = ExportUser(with_id=False, **user.model_to_dict())
                all_user_details.append(user_export_details)
            all_user_details = ExportUserList(user_list=all_user_details)
            return all_user_details
        else:
            return None

    @staticmethod
    def create_new_user_service(request_data: CreateUserRequestType) -> dict:
        user: User = UserSerializer().create(data=request_data.model_dump())
        if user:
            response = OTPServices().send_otp_to_user(user.email)
            if response == "OK":
                return {
                    "successMessage": DEFAULT_VERIFICATION_MESSAGE,
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()

    @staticmethod
    def sign_in_user(request_data: SignInRequestType) -> dict:
        response = User.authenticate_user(request_data=request_data)
        return response

    def reset_password(self, email: str) -> dict:
        if validate_user_email(email=email).is_validated:
            reset_url = self.generate_reset_password_url(email=email)
            if (
                EmailServices.send_password_reset_email_by_user_email(
                    user_email=email, reset_url=reset_url
                )
                == "OK"
            ):
                return {
                    "successMessage": "Password reset link sent successfully.",
                    "errorMessage": None,
                }
            else:
                raise EmailNotSentError()
        else:
            raise UserNotFoundError()

    @staticmethod
    def generate_reset_password_url(email: str) -> str:
        user = User.objects.get(email=email)
        token = (
            TokenGenerator()
            .get_tokens_for_user(ExportUser(**user.model_to_dict()))
            .get("access")
        )
        load_dotenv()
        FRONTEND_BASE_URL = os.environ.get("FRONTEND_BASE_URL")
        reset_url = f"{FRONTEND_BASE_URL}/password-reset/{token}/"
        return reset_url

    @staticmethod
    def change_password(uid: str, request_data: ChangePasswordRequestType):
        user = User.objects.get(id=uid)
        if validate_password(
            request_data.password1, request_data.password2
        ).is_validated:
            user.password = EncryptionServices().encrypt(request_data.password1)
            user.save()
        else:
            raise ValueError("Passwords are not matching or not in correct format.")

    @staticmethod
    def update_user_profile(uid: str, request_data: UpdateUserProfileRequestType):
        user = User.objects.get(id=uid)
        if (
            request_data.image
            and request_data.image != ""
            and request_data.image != user.image
        ):
            user.image = request_data.image
        if (
            request_data.fname
            and request_data.fname != ""
            and request_data.fname != user.fname
        ):
            if validate_name(request_data.fname).is_validated:
                user.fname = request_data.fname
        if (
            request_data.lname
            and request_data.lname != ""
            and request_data.lname != user.lname
        ):
            if validate_name(request_data.lname).is_validated:
                user.lname = request_data.lname
        if (
            request_data.dob
            and request_data.dob != ""
            and request_data.dob != user.fname
        ):
            dob = string_to_datetime(request_data.dob)
            if validate_dob(dob).is_validated:
                user.dob = dob
        if (
            request_data.phone
            and request_data.phone != ""
            and request_data.phone != user.phone
        ):
            if validate_phone(phone=request_data.phone).is_validated:
                user.phone = request_data.phone
        user.save()

    @staticmethod
    def get_user_details(uid: str) -> ExportUser:
        user = User.objects.get(id=uid)
        user_details = ExportUser(
            with_id=True, with_address=True, **user.model_to_dict()
        )
        return user_details

    @staticmethod
    def verify_user_with_otp(request_data: VerifyOTPRequestType):
        email = request_data.email
        otp = request_data.otp
        if email and validate_email_format(email) and otp and len(otp) == 6:
            user_exists = (
                True if User.objects.filter(email=email).count() > 0 else False
            )

            if user_exists:
                user = User.objects.get(email=email)
                user = ExportUser(**user.model_to_dict())
                if not user.is_active:
                    response = OTPServices().verify_otp(user, otp)
                    if response:
                        token = TokenGenerator().get_tokens_for_user(user)
                        return token
                    else:
                        raise OTPNotVerifiedError()
                else:
                    raise UserAlreadyVerifiedError()
            else:
                raise UserNotFoundError()
        else:
            raise ValueError("Email & OTP data are invalid.")
