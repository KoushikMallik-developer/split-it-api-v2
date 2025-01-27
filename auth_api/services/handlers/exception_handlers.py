import logging

import django
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyVerifiedError,
    UserNotVerifiedError,
    EmailNotSentError,
    OTPNotVerifiedError,
    UserAuthenticationFailedError,
    UserNotAuthenticatedError,
    PasswordNotMatchError,
)
from e_app.expense_exceptions.expense_exceptions import (
    ExpenseNotFoundError,
    NotAParticipantError,
)
from friends.friend_exceptions.friend_exceptions import (
    FriendNotFoundError,
    FriendRequestNotSentError,
    SelfFriendError,
    AlreadyFriendRequestSentError,
    AlreadyAFriendError,
    FriendRequestNotAcceptedError,
    FriendRequestNotFoundError,
)
from groups.group_exceptions.group_exceptions import (
    GroupNotFoundError,
    UserAlreadyInGroupError,
    MemberNotAddedError,
    NotAnGroupAdminError,
    GroupUpdateFailed,
    GroupNotCreatedError,
)


class ExceptionHandler:
    def get_handlers(self) -> dict:
        return {
            DatabaseError: {
                "message": "DatabaseError: Error Occured While Fetching details from database",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            ValidationError: {
                "message": "PydanticValidationError: Error Occured while converting to Pydantic object",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            NotImplementedError: {
                "message": "NotImplementedError",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            UserNotFoundError: {
                "message": "UserNotFoundError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            UserAlreadyVerifiedError: {
                "message": "UserAlreadyVerifiedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            UserNotVerifiedError: {
                "message": "UserNotVerifiedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            EmailNotSentError: {
                "message": "EmailNotSentError",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            OTPNotVerifiedError: {
                "message": "OTPNotVerifiedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            UserAuthenticationFailedError: {
                "message": "UserAuthenticationFailedError",
                "status": status.HTTP_401_UNAUTHORIZED,
            },
            UserNotAuthenticatedError: {
                "message": "UserNotAuthenticatedError",
                "status": status.HTTP_401_UNAUTHORIZED,
            },
            PasswordNotMatchError: {
                "message": "PasswordNotMatchError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            ValueError: {
                "message": "ValueError",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
            TokenError: {
                "message": "TokenError",
                "status": status.HTTP_401_UNAUTHORIZED,
            },
            serializers.ValidationError: {
                "message": "SerializerValidationError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            django.core.exceptions.ValidationError: {
                "message": "ValidationError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            FriendNotFoundError: {
                "message": "FriendNotFoundError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            GroupNotFoundError: {
                "message": "GroupNotFoundError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            UserAlreadyInGroupError: {
                "message": "UserAlreadyInGroupError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            MemberNotAddedError: {
                "message": "MemberNotAddedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            NotAnGroupAdminError: {
                "message": "NotAnGroupAdminError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            GroupUpdateFailed: {
                "message": "GroupUpdateFailure",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            FriendRequestNotSentError: {
                "message": "FriendRequestNotSentError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            SelfFriendError: {
                "message": "SelfFriendError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            AlreadyFriendRequestSentError: {
                "message": "AlreadyFriendRequestSentError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            AlreadyAFriendError: {
                "message": "AlreadyAFriendError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            FriendRequestNotAcceptedError: {
                "message": "FriendRequestNotAcceptedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            FriendRequestNotFoundError: {
                "message": "FriendRequestNotFoundError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            GroupNotCreatedError: {
                "message": "GroupNotCreatedError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            ExpenseNotFoundError: {
                "message": "ExpenseNotFoundError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            NotAParticipantError: {
                "message": "NotAParticipantError",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            # Exception: {
            #     "message": "InternalServerError",
            #     "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            # },
        }

    def handle_exception(self, e: Exception):
        handlers = self.get_handlers()
        for exc_type, handler in handlers.items():
            if isinstance(e, exc_type):
                logging.error(
                    f"{handler['message']}: {e.msg}"
                    if hasattr(e, "msg")
                    else f"{handler['message']}: {str(e)}"
                )
                if isinstance(e, serializers.ValidationError):
                    e.msg = "; ".join([error for error in e.detail])
                return Response(
                    data={
                        "message": (
                            f"{handler['message']}: {e.msg}"
                            if hasattr(e, "msg")
                            else f"{handler['message']}: {str(e)}"
                        ),
                    },
                    status=handler["status"],
                    content_type="application/json",
                )
        else:
            logging.error(f"InternalServerError: {e}")
            raise e
