from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from groups.export_types.request_data_type.add_member import AddMemberRequestType
from groups.services.group_services import GroupServices


class AddMemberView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:

                result = GroupServices.add_member_group_service(
                    request_data=AddMemberRequestType(**request.data), uid=user_id
                )
                return Response(
                    data={
                        "message": result.get("message"),
                        "data": result.get("data"),
                    },
                    status=status.HTTP_201_CREATED,
                    content_type="application/json",
                )
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
