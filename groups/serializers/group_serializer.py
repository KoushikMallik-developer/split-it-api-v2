from typing import Optional, List

from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_email, validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError
from friends.models.friend import Friend
from groups.export_types.create_group import CreateGroupRequestType
from groups.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: CreateGroupRequestType = data.get("request_data")
        uid: str = data.get("uid")

        members = request.members
        name = request.name

        if name and Group.objects.filter(name=name, creator_id=uid).exists():
            raise ValueError(f"A group with the name '{name}' already exists.")

        if members:
            for member in members:
                if not User.objects.filter(email=member).exists():
                    raise UserNotFoundError(msg=f"User '{member}' does not exist.")
                if not Friend.objects.filter(user2__id=uid, user1__id=User.objects.get(email=member).id).exists():
                    raise FriendNotFoundError(msg=f"'{member}' is not your friend.")

        return True

    def create(self, data: dict) -> Group:
        request: CreateGroupRequestType = data.get("request_data")
        uid: str = data.get("uid")

        creator: User = User.objects.get(id=uid)

        members = request.members
        name = request.name
        image = request.image

        if self.validate(data):
            list_members: List[User] = []

            if not members:
                list_members.append(creator)
            else:
                for member_email in members:
                    if member_email and member_email != "" and isinstance(member_email, str):
                        validation_result_email: ValidationResult = validate_user_email(member_email)
                        is_validated_email = validation_result_email.is_validated
                        if not is_validated_email:
                            raise serializers.ValidationError(detail=validation_result_email.error)

                        user_friends: User = User.objects.get(email=member_email)
                        list_members.append(user_friends)

            list_members.insert(0, creator)

            group = Group.objects.create(name=name, image=image, creator=creator)

            group.members.set(list_members)
            if group:
                group.save()
                return group
