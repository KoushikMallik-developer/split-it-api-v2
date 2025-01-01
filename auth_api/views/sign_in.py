from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_api.export_types.request_data_types.sign_in import SignInRequestType
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.user_services.user_services import UserServices


class SignInView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            request_data = request.data
            email = request_data.get("email")
            password = request_data.get("password")

            if email and password:
                result = UserServices.sign_in_user(
                    request_data=SignInRequestType(**request_data)
                )
                if result.get("token"):
                    return Response(
                        data={"token": result.get("token"), "errorMessage": None},
                        status=status.HTTP_200_OK,
                        content_type="application/json",
                    )
            else:
                raise ValueError("Email or Password is not in correct format")

        except Exception as e:
            return ExceptionHandler().handle_exception(e)
