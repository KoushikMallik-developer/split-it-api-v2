from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.models.user_models.user import User
from auth_api.services.helpers import is_valid_uuid
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError


class RemoveFriendSerializer(serializers.ModelSerializer):
    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        # User uuid Validation
        if not data.get("user_id") or not isinstance(data.get("user_id"), str):
            raise ValueError("User ID is required.")

        if not is_valid_uuid(value=data.get("user_id")):
            raise ValueError("User ID is not valid.")

        # Check if the friend exists with the provided email
        try:
            user: User = User.objects.get(id=data.get("primary_user_id"))
            friend_exists = user.friends.filter(id=data.get("user_id")).exists()
            if not friend_exists:
                raise FriendNotFoundError()
        except ObjectDoesNotExist:
            raise UserNotFoundError(msg="This user is not registered with us.")

        # validated
        return True

    def remove_friend(self, data: dict):
        if self.validate(data=data):
            user_id = data.get("primary_user_id")
            friend_id = data.get("user_id")
            try:
                user = User.objects.get(id=user_id)
                friend = user.friends.get(id=friend_id)
                user.friends.remove(friend)
                friend.friends.remove(user)
                friend.save()
                user.save()
            except ObjectDoesNotExist:
                raise UserNotFoundError(msg="This user is not registered with us.")
