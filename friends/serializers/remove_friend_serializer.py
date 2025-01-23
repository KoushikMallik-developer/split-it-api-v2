from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendNotFoundError


class RemoveFriendSerializer(serializers.ModelSerializer):
    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
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
        user: User = User.objects.get(id=data.get("primary_user_id"))
        friend_exists = user.friends.filter(email=data.get("user_email")).exists()
        if not friend_exists:
            raise FriendNotFoundError()

        # validated
        return True

    def remove_friend(self, data: dict):
        if self.validate(data=data):
            user_id = data.get("primary_user_id")
            friend_email = data.get("user_email")
            try:
                user = User.objects.get(id=user_id)
                friend = user.friends.get(email=friend_email)
                user.friends.remove(friend)
                user.save()
            except ObjectDoesNotExist:
                raise UserNotFoundError(msg="This user is not registered with us.")
