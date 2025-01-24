from typing import Optional
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotAuthenticatedError,
)
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import (
    SelfFriendError,
    AlreadyFriendRequestSentError,
    AlreadyAFriendError,
)
from friends.models.friend_request import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        sender: User = User.objects.get(id=data.get("sender"))
        if not sender:
            raise UserNotAuthenticatedError()

        # Email Validation
        if data.get("receiver") and isinstance(data.get("receiver"), str):
            validation_result_email: ValidationResult = validate_user_email(
                data.get("receiver")
            )
            if not validation_result_email.is_validated:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("user_email is required.")

        receiver: User = User.objects.get(email=data.get("receiver"))

        # Check if the user has already sent friend request to the same user.
        already_sent_request: bool = (
            FriendRequest.objects.filter(
                sender__id=sender.id, receiver__id=receiver.id
            ).exists()
            or FriendRequest.objects.filter(
                sender__id=receiver.id, receiver__id=sender.id
            ).exists()
        )
        if already_sent_request:
            raise AlreadyFriendRequestSentError()

        # Check if the user is already friends with the same user.
        already_a_friend: bool = (
            sender.friends.filter(id=receiver.id).exists()
            or receiver.friends.filter(id=sender.id).exists()
        )
        if already_a_friend:
            raise AlreadyAFriendError()

        # Check if the user is sending friend request to himself.
        is_self_user: bool = True if sender.id == receiver.id else False
        if is_self_user:
            raise SelfFriendError()
        # validated user
        return True

    def create(self, data: dict) -> FriendRequest:
        if self.validate(data=data):
            sender: User = User.objects.get(id=data.get("sender"))
            receiver: User = User.objects.get(email=data.get("receiver"))
            new_friend_request = FriendRequest(sender=sender, receiver=receiver)
            new_friend_request.save()
            return new_friend_request
