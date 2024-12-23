from typing import Optional

from django.db.models import Q
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
from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest


class AcceptFriendRequestSerializer(serializers.ModelSerializer):
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
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("user_email is required.")

        receiver: User = User.objects.get(email=data.get("receiver"))

        # Check if the user is already friends with the same user.
        already_a_friend: bool = Friend.objects.filter(
            Q(user1__id=sender.id, user2__id=receiver.id)
            | Q(user1__id=receiver.id, user2__id=sender.id)
        ).exists()
        if already_a_friend:
            raise AlreadyAFriendError()

        # validated user
        return True

    def create(self, data: dict) -> Friend:
        if self.validate(data=data):
            sender: User = User.objects.get(id=data.get("sender"))
            receiver: User = User.objects.get(email=data.get("receiver"))

            get_new_friend_request: FriendRequest = FriendRequest.objects.get(sender__id=sender.id,
                                                                              receiver__id=receiver.id)
            get_new_friend_request.delete()

            new_friend: Friend = Friend(user1=sender, user2=receiver)
            new_friend.save()

            return new_friend
