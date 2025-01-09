from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_api.export_types.request_data_types.create_user import CreateUserRequestType
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.user_services.user_services import UserServices


class CreateUsersView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            result = UserServices.create_new_user_service(
                request_data=CreateUserRequestType(**request.data)
            )
            if result.get("successMessage"):
                return Response(
                    data={
                        "message": result.get("successMessage"),
                    },
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
