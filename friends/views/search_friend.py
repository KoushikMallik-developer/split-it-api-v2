from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from friends.export_types.request_data_types.search_friend import (
    SearchFriendRequestType,
)
from friends.services.friends_services import UseFriendServices


class SearchFriendView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                searched_friends = UseFriendServices.get_searched_friends(
                    request_data=SearchFriendRequestType(**request.data),
                    user_id=user_id,
                )
                return Response(
                    data={
                        "data": (searched_friends if searched_friends else []),
                        "message": (
                            "Search results fetched successfully"
                            if searched_friends
                            else "No result found"
                        ),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
