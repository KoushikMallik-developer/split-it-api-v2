from django.core.exceptions import ObjectDoesNotExist

from auth_api.models.user_models.user import User
from groups.export_types.add_member import AddMemberRequestType
from groups.export_types.create_group import CreateGroupRequestType
from groups.export_types.update_group import UpdateGroupRequestType
from groups.group_exceptions.group_exceptions import (
    MemberNotAddedError,
    GroupNotFoundError,
    NotAnGroupAdminError,
    GroupUpdateFailure,
)
from groups.models.group import Group
from groups.serializers.add_member_serializer import AddMemberSerializer
from groups.serializers.group_serializer import GroupSerializer


class GroupServices:
    @staticmethod
    def create_new_group_service(
        request_data: CreateGroupRequestType, uid: str
    ) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        group: Group = GroupSerializer().create(data)
        print(f"Group {group.id} is created")
        return {
            "successMessage": f"Group {group.name} is created",
            "errorMessage": None,
        }

    @staticmethod
    def add_member_group_service(request_data: AddMemberRequestType, uid: str) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        user: User = AddMemberSerializer().create(data)
        if user:
            return {
                "successMessage": f"Member {user.fname} {user.lname} is added",
                "errorMessage": None,
            }
        else:
            raise MemberNotAddedError()

    @staticmethod
    def update_group(uid: str, request_data: UpdateGroupRequestType):
        try:
            group: Group = Group.objects.get(id=request_data.group_id)

            if str(group.creator.id) != uid:
                raise NotAnGroupAdminError()

            if not request_data.name and not request_data.image:
                raise GroupUpdateFailure()

            if request_data.name and isinstance(request_data.name, str):
                group.name = request_data.name

            if request_data.image and isinstance(request_data.image, str):
                group.image = request_data.image

            group.save()

        except ObjectDoesNotExist:
            raise GroupNotFoundError()
