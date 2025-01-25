from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.models.user_models.user import User
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
        user_id = request.user_id

        creator: User = User.objects.get(id=uid)
        group: Group = Group.objects.get(id=group_id)

        if str(group.creator.id) != uid:
            raise NotAnGroupAdminError()

        if not User.objects.filter(id=user_id).exists():
            raise UserNotFoundError(msg="This user is not registered with us.")

        if not creator.friends.filter(id=user_id).exists():
            raise FriendNotFoundError(msg="This user is not your friend.")

        if not validate_group_uid(group_uid=group_id).is_validated:
            raise GroupNotFoundError()

        member: User = User.objects.get(id=user_id)

        if group.members.filter(id=member.id).exists():
            raise UserAlreadyInGroupError()

        return True

    def create(self, data: dict) -> Group:
        try:
            request: AddMemberRequestType = data.get("request_data")

            user_id: str = request.user_id
            group_id: str = request.group_id

            if self.validate(data):
                group: Group = Group.objects.get(id=group_id)
                user: User = User.objects.get(id=user_id)

                group.members.add(user)
                group.save()

                return group
        except ObjectDoesNotExist:
            raise GroupNotFoundError()
