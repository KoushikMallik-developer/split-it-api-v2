import logging

from psycopg2 import DatabaseError
from pydantic import ValidationError
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from friends.services.friends_services import UseFriendServices


class AllFriendsView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                friends = UseFriendServices.get_all_friends_service(user_id)
                return Response(
                    data={
                        "data": friends.model_dump() if friends is not None else {},
                        "errorMessage": None,
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                logging.warning("No User found in database.")
                raise Exception("No User found in database.")
        except DatabaseError as e:
            logging.error(
                f"DatabaseError: Error Occured While Fetching all users details: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"DatabaseError: Error Occured While Fetching all users details: {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
        except ValidationError as e:
            logging.error(
                f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}"
            )
            return Response(
                data={
                    "successMessage": None,
                    "errorMessage": f"PydanticValidationError: Error Occured while converting to Pydantic object: {e}",
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
                    "errorMessage": f"InternalServerError {e}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type="application/json",
            )
