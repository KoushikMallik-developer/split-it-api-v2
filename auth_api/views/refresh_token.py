from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from auth_api.models.user_models.user import User
from auth_api.services.handlers.exception_handlers import ExceptionHandler


class RefreshTokenView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                raise ValueError("Refresh token is required.")

            refresh = RefreshToken(refresh_token)
            refresh.verify()
            user_id = refresh["user_id"]
            user = User.objects.get(id=user_id)

            new_refresh = RefreshToken.for_user(user)
            new_access_token = str(new_refresh.access_token)

            return Response(
                data={
                    "message": "Refreshed access token successfully.",
                    "access": new_access_token,
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
