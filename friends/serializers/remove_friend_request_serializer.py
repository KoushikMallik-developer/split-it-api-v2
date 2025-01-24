from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
)
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import FriendRequestNotFoundError
from friends.models.friend_request import FriendRequest


class RemoveFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        friend_request_email: str = data.get("friend_request_email")

        # Email Validation
        if friend_request_email and isinstance(friend_request_email, str):
            validation_result_email: ValidationResult = validate_user_email(
                friend_request_email
            )
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("Email is required.")

        # checking the provided email is part of the friend request list
        existing_friend_request = FriendRequest.objects.filter(
            Q(sender__email=friend_request_email)
            | Q(receiver__email=friend_request_email)
        ).exists()

        if not existing_friend_request:
            raise FriendRequestNotFoundError()

        # validated
        return True

    def remove_friend_request(self, data: dict):
        if self.validate(data=data):
            user_id: str = data.get("primary_user_id")
            friend_request_email: str = data.get("friend_request_email")
            try:
                existing_friend_request: FriendRequest = FriendRequest.objects.get(
                    Q(sender__id=user_id, receiver__email=friend_request_email)
                    | Q(receiver__id=user_id, sender__email=friend_request_email)
                )

                existing_friend_request.delete()
            except ObjectDoesNotExist:
                raise FriendRequestNotFoundError()
