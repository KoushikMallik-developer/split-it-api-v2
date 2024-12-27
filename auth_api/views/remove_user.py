from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
)
from auth_api.models.user_models.user import User
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import validate_user_email


class RemoveUserView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            email = request.data.get("email")
            if validate_user_email(email=email).is_validated:
                User.objects.get(email=email).delete()
                return Response(
                    data={
                        "successMessage": "User removed Successfully.",
                        "errorMessage": None,
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise UserNotFoundError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
