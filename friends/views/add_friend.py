from rest_framework.request import Request
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from friends.export_types.request_data_types.add_friend import AddFriendRequestType
from friends.services.friends_services import UseFriendServices


class AddFriend(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                result = UseFriendServices.create_new_friend_request_service(
                    request_data=AddFriendRequestType(**request.data), uid=user_id
                )
                return Response(
                    data={
                        "message": (
                            result.get("message")
                            if result.get("message")
                            else "Friend request sent"
                        ),
                    },
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )

            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
