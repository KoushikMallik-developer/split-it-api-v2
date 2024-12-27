from auth_api.auth_exceptions.user_exceptions import (
    UserNotVerifiedError,
    UserAuthenticationFailedError,
    UserNotFoundError,
)
from auth_api.export_types.request_data_types.sign_in import SignInRequestType
from auth_api.export_types.user_types.export_user import ExportUser
from auth_api.models.user_models.abstract_user import AbstractUser
from auth_api.services.encryption_services.encryption_service import EncryptionServices
from auth_api.services.token_services.token_generator import TokenGenerator


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def authenticate_user(request_data: SignInRequestType) -> dict:
        if request_data.email and request_data.password:
            user_exists = (
                True
                if User.objects.filter(email=request_data.email).count() > 0
                else False
            )
            if user_exists:
                user = User.objects.get(email=request_data.email)
                if user:
                    if (
                        EncryptionServices().decrypt(user.password)
                        == request_data.password
                    ):
                        if user.is_active:
                            token = TokenGenerator().get_tokens_for_user(
                                ExportUser(**user.model_to_dict())
                            )
                            return {
                                "token": token,
                                "errorMessage": None,
                            }
                        else:
                            raise UserNotVerifiedError()
                    else:
                        raise UserAuthenticationFailedError()
                else:
                    raise UserNotFoundError()
            else:
                raise UserNotFoundError()
        else:
            raise ValueError("Provided Email or Password is invalid.")
