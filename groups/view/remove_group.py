from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from groups.export_types.request_data_type.delete_group import DeleteGroupRequestType
from groups.services.group_services import GroupServices


class RemoveGroupView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                GroupServices().remove_group(
                    uid=user_id,
                    request_data=DeleteGroupRequestType(**request.data),
                )
                return Response(
                    data={
                        "data": None,
                        "message": "Group deleted successfully.",
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
