from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotAuthenticatedError,
)
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import (
    AlreadyAFriendError,
    FriendRequestNotFoundError,
)
from friends.models.friend_request import FriendRequest


class AcceptFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:

        # Email Validation
        if data.get("sender") and isinstance(data.get("sender"), str):
            validation_result_email: ValidationResult = validate_user_email(
                data.get("sender")
            )
            if not validation_result_email.is_validated:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("user_email is required.")

        sender: User = User.objects.get(email=data.get("sender"))

        receiver: User = User.objects.get(id=data.get("receiver"))
        if not receiver:
            raise UserNotAuthenticatedError()

        # Check if the user is already friends with the same user.
        already_a_friend: bool = (
            sender.friends.filter(id=receiver.id).exists()
            or receiver.friends.filter(id=sender.id).exists()
        )
        if already_a_friend:
            raise AlreadyAFriendError()

        # validated user
        return True

    def create(self, data: dict):
        if self.validate(data=data):
            try:
                sender: User = User.objects.get(email=data.get("sender"))
                receiver: User = User.objects.get(id=data.get("receiver"))

                existing_friend_request: FriendRequest = FriendRequest.objects.get(
                    sender__id=sender.id, receiver__id=receiver.id
                )

                existing_friend_request.delete()

                sender.friends.add(receiver)
                receiver.friends.add(sender)

                sender.save()
                receiver.save()
            except ObjectDoesNotExist:
                raise FriendRequestNotFoundError()
