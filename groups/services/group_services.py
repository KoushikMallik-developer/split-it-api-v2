from groups.export_types.create_group import CreateGroupRequestType
from groups.models.group import Group
from groups.serializers.group_serializer import GroupSerializer


class GroupServices:
    @staticmethod
    def create_new_group_service(
        request_data: CreateGroupRequestType, uid: str
    ) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        group: Group = GroupSerializer().create(data)
        return {
            "successMessage": f"Group {group.name} is created",
            "errorMessage": None,
        }
