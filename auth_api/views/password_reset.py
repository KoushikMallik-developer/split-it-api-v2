from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
)
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.user_services.user_services import UserServices


class PasswordResetView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            email = request.data.get("email")
            if email:
                result = UserServices().reset_password(email=email)
                return Response(
                    data={
                        "message": result.get("successMessage"),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise UserNotFoundError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
