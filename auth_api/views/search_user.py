from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from auth_api.export_types.user_types.search_user import SearchUserRequestType
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from auth_api.services.user_services.user_services import UserServices


class SearchUsersView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                searched_friends = UserServices.get_searched_users(
                    request_data=SearchUserRequestType(**request.data)
                )
                return Response(
                    data={
                        "data": (
                            searched_friends.model_dump()
                            if searched_friends is not None
                            else []
                        ),
                        "message": (
                            "Users are fetched"
                            if searched_friends is not None
                            else "No User found"
                        ),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
