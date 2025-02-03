from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from groups.export_types.request_data_type.get_group_by_id_request_type import (
    GetGroupByIdRequestType,
)
from groups.services.group_services import GroupServices


class GetGroupByIdView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                result = GroupServices().get_group_by_id_service(
                    data=GetGroupByIdRequestType(**request.data), uid=user_id
                )
                return Response(
                    data={
                        "data": result.get("data") if result.get("data") else {},
                        "message": (
                            result.get("message")
                            if result.get("message")
                            else "Groups fetched successfully"
                        ),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )
            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
