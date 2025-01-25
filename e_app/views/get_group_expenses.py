from rest_framework.request import Request
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from e_app.export_types.request_data_types.get_group_expense_request_type import (
    GetGroupExpenseRequestType,
)
from e_app.services.expense_services import ExpenseService


class GetGroupExpenses(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:
                result = ExpenseService().get_group_expense_service(
                    data=GetGroupExpenseRequestType(**request.data), uid=user_id
                )
                return Response(
                    data={
                        "message": "Expenses fetched successfully",
                        "data": result,
                    },
                    status=status.HTTP_200_OK,
                    content_type="application/json",
                )

            else:
                raise TokenError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
