from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotAuthenticatedError,
)
from auth_api.models.user_models.user import User
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import (
    validate_user_email,
    decode_jwt_token,
    validate_user_uid,
)


class RemoveUserView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                email = request.data.get("email")
                if not email:
                    raise ValueError("Email is required.")
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
            else:
                raise UserNotAuthenticatedError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
