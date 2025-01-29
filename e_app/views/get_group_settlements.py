from rest_framework.request import Request
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from e_app.export_types.request_data_types.get_group_settlements_request_type import (
    GetGroupSettlementsRequestType,
)
from e_app.services.settlement_services import SettlementService


class GetGroupSettlements(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                result = SettlementService().get_group_settlements(
                    data=GetGroupSettlementsRequestType(**request.data)
                )
                return Response(
                    data={
                        "message": "Settlements fetched successfully",
                        "data": result.get("data"),
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )

            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
