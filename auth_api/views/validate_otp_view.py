from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_api.export_types.request_data_types.verify_otp import VerifyOTPRequestType
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.user_services.user_services import UserServices


class ValidateOTPView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            token = UserServices().verify_user_with_otp(
                request_data=VerifyOTPRequestType(**request.data)
            )
            return Response(
                data={
                    "token": token,
                    "message": None,
                },
                status=status.HTTP_200_OK,
                content_type="application/json",
            )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
