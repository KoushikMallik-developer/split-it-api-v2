from typing import Optional

from django.db.models import Q
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import (
    FriendNotFoundError,
    NoFriendsError,
)

from friends.models.friend import Friend


class RemoveFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        user_id: str = data.get("primary_user_id")

        # Check if the user has any friends
        friends = Friend.objects.filter(Q(user1__id=user_id) | Q(user2__id=user_id))
        if not friends.exists():
            raise NoFriendsError()

        # Email Validation
        if data.get("user_email") and isinstance(data.get("user_email"), str):
            validation_result_email: ValidationResult = validate_user_email(
                data.get("user_email")
            )
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("user_email is required.")

        # Check if the friend exists with the provided email
        friend_exists = friends.filter(
            Q(user1__email=data.get("user_email"))
            | Q(user2__email=data.get("user_email"))
        ).exists()
        if not friend_exists:
            raise FriendNotFoundError()

        # validated
        return True

    def remove_friend(self, data: dict) -> Friend:
        if self.validate(data=data):
            user_id = data.get("primary_user_id")
            friend_email = data.get("user_email")

            '''The current user (user_id) is user1 and their friend has the email (friend_email) as user2.
            The current user (user_id) is user2 and their friend has the email (friend_email) as user1.'''
            friend: Friend = Friend.objects.filter(
                Q(user1__id=user_id, user2__email=friend_email)
                | Q(user2__id=user_id, user1__email=friend_email)
            ).first()

            if friend:
                friend.delete()
                return friend
