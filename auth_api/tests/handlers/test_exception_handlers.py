from rest_framework import status

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyVerifiedError,
    UserNotVerifiedError,
    EmailNotSentError,
    OTPNotVerifiedError,
    UserAuthenticationFailedError,
    UserNotAuthenticatedError,
)
from auth_api.services.handlers.exception_handlers import ExceptionHandler


class TestExceptionHandler:
    def test_handle_exception_user_not_found(self):
        handler = ExceptionHandler()
        exception = UserNotFoundError("User not found")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "UserNotFoundError: User not found"

    def test_handle_exception_user_already_verified(self):
        handler = ExceptionHandler()
        exception = UserAlreadyVerifiedError("User already verified")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserAlreadyVerifiedError: User already verified"
        )

    def test_handle_exception_user_not_verified(self):
        handler = ExceptionHandler()
        exception = UserNotVerifiedError("User not verified")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "UserNotVerifiedError: User not verified"

    def test_handle_exception_email_not_sent(self):
        handler = ExceptionHandler()
        exception = EmailNotSentError("Email not sent")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["message"] == "EmailNotSentError: Email not sent"

    def test_handle_exception_otp_not_verified(self):
        handler = ExceptionHandler()
        exception = OTPNotVerifiedError("OTP not verified")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "OTPNotVerifiedError: OTP not verified"

    def test_handle_exception_user_authentication_failed(self):
        handler = ExceptionHandler()
        exception = UserAuthenticationFailedError("Password is invalid")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserAuthenticationFailedError: Password is invalid"
        )

    def test_handle_exception_user_not_authenticated(self):
        handler = ExceptionHandler()
        exception = UserNotAuthenticatedError("User not authenticated")
        response = handler.handle_exception(exception)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserNotAuthenticatedError: User not authenticated"
        )
