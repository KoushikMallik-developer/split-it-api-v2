from typing import Optional, List

from rest_framework import serializers

from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_uid
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError
from groups.export_types.request_data_type.create_group import CreateGroupRequestType
from groups.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: CreateGroupRequestType = data.get("request_data")
        uid: str = data.get("uid")

        user = User.objects.get(id=uid)

        members = request.members
        name = request.name

        if name and Group.objects.filter(name=name, creator_id=uid).exists():
            raise ValueError(f"A group with the name '{name}' already exists.")

        if members:
            for member_id in members:

                # check if the member is a valid email
                if member_id and member_id != "" and isinstance(member_id, str):
                    validation_result: ValidationResult = validate_user_uid(member_id)
                    is_validated = validation_result.is_validated
                    if not is_validated:
                        raise serializers.ValidationError(
                            detail=f"{member_id} does not exist."
                        )

                # check if the member is a friend
                if not user.friends.filter(id=member_id).exists():
                    raise FriendNotFoundError(msg=f"'{member_id}' is not your friend.")

        return True

    def create(self, data: dict) -> Group:
        request: CreateGroupRequestType = data.get("request_data")
        uid: str = data.get("uid")

        creator: User = User.objects.get(id=uid)

        members = request.members
        name = request.name
        image = request.image
        description = request.description

        if self.validate(data):
            list_members: List[User] = [creator]

            if members and len(members) > 0:
                for member_id in members:
                    list_members.append(User.objects.get(id=member_id))

            group = Group.objects.create(
                name=name, image=image, creator=creator, description=description
            )
            group.members.set(list_members)
            group.save()

            return group
