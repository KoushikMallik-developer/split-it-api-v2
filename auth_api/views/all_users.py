from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.export_types.user_types.export_user import ExportUserList
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.user_services.user_services import UserServices


class AllUsersView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, _):
        try:
            all_user_details = UserServices.get_all_users_service()
            if all_user_details and isinstance(all_user_details, ExportUserList):
                return Response(
                    data={
                        "data": all_user_details.model_dump(),
                        "message": None,
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                return Response(
                    data={
                        "data": {"user_list": []},
                        "message": "No User found in database.",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
