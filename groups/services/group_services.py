from auth_api.models.user_models.user import User
from groups.export_types.add_member import AddMemberRequestType
from groups.export_types.create_group import CreateGroupRequestType
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
    def add_member_group_service(
        request_data: AddMemberRequestType, uid: str
    ) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        AddMemberSerializer().create(data)
        return {
            "successMessage": f"Member is added",
            "errorMessage": None,
        }
