from typing import Optional

from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError
from groups.export_types.request_data_type.add_member import AddMemberRequestType
from groups.group_exceptions.group_exceptions import (
    GroupNotFoundError,
    UserAlreadyInGroupError,
    NotAnGroupAdminError,
)
from groups.models.group import Group
from groups.services.group_helpers import validate_group_uid


class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: AddMemberRequestType = data.get("request_data")
        uid: str = data.get("uid")

        group_id = request.group_id
        user_email = request.user_email

        user = User.objects.get(id=uid)
        group: Group = Group.objects.get(id=group_id)

        if str(group.creator.id) != uid:
            raise NotAnGroupAdminError()

        if not validate_user_email(user_email).is_validated:
            raise UserNotFoundError(msg="This user is not registered with us.")
        if not user.friends.filter(email=user_email).exists():
            raise FriendNotFoundError(msg=f"'{user_email}' is not your friend.")

        if not validate_group_uid(group_uid=group_id).is_validated:
            raise GroupNotFoundError()

        member: User = User.objects.get(email=user_email)

        if group.members.filter(id=member.id).exists():
            raise UserAlreadyInGroupError()

        return True

    def create(self, data: dict) -> Group:
        request: AddMemberRequestType = data.get("request_data")

        user_email: str = request.user_email
        group_id: str = request.group_id

        if self.validate(data):
            group: Group = Group.objects.get(id=group_id)
            user: User = User.objects.get(email=user_email)

            group.members.add(user)
            group.save()

            return group
