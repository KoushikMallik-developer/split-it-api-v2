from typing import List

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_api.services.handlers.exception_handlers import ExceptionHandler
from auth_api.services.helpers import decode_jwt_token, validate_user_uid
from groups.export_types.create_group import CreateGroupRequestType
from groups.group_exceptions.group_exceptions import GroupCantCreateError
from groups.services.group_services import GroupServices


class CreateGroupView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request: Request):
        try:
            user_id = decode_jwt_token(request=request)
            if validate_user_uid(uid=user_id).is_validated:

                name = request.data.get("name")
                if not name or name == "":
                    raise ValueError("Group name should not be empty")

                members = request.data.get("members")
                if not isinstance(members, List):
                    raise ValueError("members should be a list of string")

                result = GroupServices.create_new_group_service(
                    request_data=CreateGroupRequestType(**request.data), uid=user_id
                )
                if result.get("successMessage"):
                    return Response(
                        data={
                            "successMessage": result.get("successMessage"),
                            "errorMessage": None,
                        },
                        status=status.HTTP_201_CREATED,
                        content_type="application/json",
                    )
                else:
                    raise GroupCantCreateError()
        except Exception as e:
            return ExceptionHandler().handle_exception(e)
