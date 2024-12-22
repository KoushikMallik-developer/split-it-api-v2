import logging
from rest_framework.request import Request
from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from friends.export_types.request_data_types.add_friend import AddFriendRequestType
from friends.friend_exceptions.friend_exceptions import (
    SelfFriendError,
    AlreadyFriendRequestSentError,
    ReversedFriendRequestError,
    AlreadyAFriendError,
)
from friends.services.friends_services import UseFriendServices


class AcceptFriendRequest(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                result = {}
                if result.get("successMessage"):
                    return Response(
                        data={
                            "data": result.get("successMessage"),
                            "errorMessage": None,
                        },
                        status=status.HTTP_200_OK,
                        content_type="application/json",
                    )
                else:
                    return Response(
                        data={
                            "data": result.get("errorMessage"),
                            "errorMessage": None,
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type="application/json",
                    )
            else:
                logging.warning("No User found in database.")
                raise Exception("No User found in database.")
        except UserNotFoundError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"UserNotFoundError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except SelfFriendError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"SelfFriendError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except AlreadyFriendRequestSentError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"AlreadyFriendRequestSentError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ReversedFriendRequestError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"ReversedFriendRequestError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except AlreadyAFriendError as e:
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"AlreadyAFriendError: {e.msg}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occurred While Fetching all users details: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"DatabaseError: Error Occurred While Fetching all users details: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occurred while converting to Pydantic object: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"PydanticValidationError: Error Occurred while converting to Pydantic object: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except NotImplementedError as e:
            logging.warning(f"Internal Server Error: {e}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"NotImplementedError: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except Exception as e:
            logging.error(f"InternalServerError: {e}")
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"InternalServerError: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
