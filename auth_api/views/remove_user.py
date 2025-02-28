from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.auth_exceptions.user_exceptions import (
    UserNotAuthenticatedError,
)
from auth_api.models.user_models.user import User
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import (
    decode_jwt_token,
    validate_user_uid,
)


class RemoveUserView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                user = User.objects.get(id=user_id, is_deleted=False)
                user.is_deleted = True
                user.save()
                return Response(
                    data={
                        "message": "User removed Successfully.",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise UserNotAuthenticatedError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
