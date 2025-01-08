from typing import Optional

from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError
from friends.models.friend import Friend
from groups.export_types.add_member import AddMemberRequestType
from groups.group_exceptions.group_exceptions import (
    GroupNotFoundError,
    UserAlreadyInGroupError,
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

        if user_email:
            validation_result_email: ValidationResult = validate_user_email(user_email)
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise UserNotFoundError(msg="This user is not registered with us.")
            if (
                not Friend.objects.filter(
                    user2__id=uid, user1__id=User.objects.get(email=user_email).id
                ).exists()
                and not Friend.objects.filter(
                    user2__id=User.objects.get(email=user_email).id, user1__id=uid
                ).exists()
            ):
                raise FriendNotFoundError(msg=f"'{user_email}' is not your friend.")

        if group_id:
            if not validate_group_uid(group_uid=group_id).is_validated:
                raise GroupNotFoundError()

            group: Group = Group.objects.get(id=group_id)
            user: User = User.objects.get(email=user_email)

            if group.members.get(id=user.id):
                raise UserAlreadyInGroupError()

        return True

    def create(self, data: dict) -> User:
        request: AddMemberRequestType = data.get("request_data")

        user_email: str = request.user_email
        group_id: str = request.group_id

        if self.validate(data):
            group: Group = Group.objects.get(id=group_id)
            user: User = User.objects.get(email=user_email)

            group.members.add(user)

            return user
