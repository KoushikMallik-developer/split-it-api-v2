from typing import Optional, List

from rest_framework import serializers

from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError
from friends.models.friend import Friend
from groups.export_types.add_member import AddMemberRequestType
from groups.export_types.create_group import CreateGroupRequestType
from groups.models.group import Group


class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        request: AddMemberRequestType = data.get("request_data")
        uid: str = data.get("uid")

        group_id = request.group_id
        user_email = request.user_email

        # if name and Group.objects.filter(name=name, creator_id=uid).exists():
        #     raise ValueError(f"A group with the name '{name}' already exists.")
        #
        # if members:
        #     for member_email in members:
        #
        #         # check if the member is a valid email
        #         if (
        #             member_email
        #             and member_email != ""
        #             and isinstance(member_email, str)
        #         ):
        #             validation_result_email: ValidationResult = validate_user_email(
        #                 member_email
        #             )
        #             is_validated_email = validation_result_email.is_validated
        #             if not is_validated_email:
        #                 raise serializers.ValidationError(
        #                     detail=f"{member_email} does not exist."
        #                 )
        #
        #         # check if the member is a friend
        #         if not Friend.objects.filter(
        #             user2__id=uid, user1__id=User.objects.get(email=member_email).id
        #         ).exists():
        #             raise FriendNotFoundError(
        #                 msg=f"'{member_email}' is not your friend."
        #             )

        return True

    def create(self, data: dict) -> User:
        request: AddMemberRequestType = data.get("request_data")
        uid: str = data.get("uid")

        creator: User = User.objects.get(id=uid)

        user_email: str = request.user_email
        group_id: str = request.group_id

        group: Group = Group.objects.filter(id=group_id).first()

        if self.validate(data):
            # list_members: List[User] = [creator]
            #
            # if members and len(members) > 0:
            #     for member_email in members:
            #         list_members.append(User.objects.get(email=member_email))
            #
            # group = Group.objects.create(name=name, image=image, creator=creator)
            # group.members.set(list_members)

            return creator
