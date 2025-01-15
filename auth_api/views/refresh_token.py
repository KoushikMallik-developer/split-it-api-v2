from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from auth_api.services.handlers.exception_handlers import ExceptionHandler


class RefreshTokenView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                raise ValueError("Refresh token is required.")

            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

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
