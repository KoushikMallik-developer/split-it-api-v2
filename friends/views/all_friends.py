from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from auth_api.services.handlers.exception_handlers import ExceptionHandler
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
                        "data": friends if friends is not None else [],
                        "message": "All friends fetched successfully",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
