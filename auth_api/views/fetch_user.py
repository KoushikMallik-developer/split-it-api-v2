from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import validate_user_uid
from auth_api.services.user_services.user_services import UserServices


class FetchUserView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request: Request):
        try:
            request_data = request.data
            user_id = request_data.get("user_id")
            if not user_id:
                raise ValueError("User ID is required.")
            if validate_user_uid(uid=user_id).is_validated:
                user_details = UserServices().get_user_details(uid=user_id)
                return Response(
                    data={
                        "message": "User details fetched successfully.",
                        "data": user_details.model_dump(),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
