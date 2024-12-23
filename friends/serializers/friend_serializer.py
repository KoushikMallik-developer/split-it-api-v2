from typing import Optional

from django.db.models import Q
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_user_email
from friends.friend_exceptions.friend_exceptions import (
    SelfFriendError,
    AlreadyFriendRequestSentError,
    ReversedFriendRequestError,
    AlreadyAFriendError,
)
from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, sender: User, data: Optional[dict] = None) -> Optional[bool]:
        is_validated_email = False
        email = data.get("email")

        receiver: User = User.objects.get(email=email)
        sender: User = sender

        already_sent_request: bool = FriendRequest.objects.filter(
            sender=sender, receiver=receiver
        ).exists()

        reversed_sent_request: bool = FriendRequest.objects.filter(
            sender=receiver, receiver=sender
        ).exists()

        already_a_friend: bool = Friend.objects.filter(
            Q(user1=sender, user2=receiver) | Q(user1=receiver, user2=sender)
        ).exists()

        is_self_user: bool = True if sender.id == receiver.id else False

        receiver_info: str = (
            receiver.username.upper() if receiver.username else receiver.email
        )

        # Friend request receiver Email Validation
        if email and isinstance(email, str):
            validation_result_email: ValidationResult = validate_user_email(email)
            is_validated_email = validation_result_email.is_validated

            # user not found
            if not is_validated_email:
                raise UserNotFoundError(msg="This user not registered with us.")

            # sender cant be receiver
            if is_self_user:
                raise SelfFriendError()

            # Check if a friend request already exists
            if already_sent_request:
                raise AlreadyFriendRequestSentError()

            # Check if the reverse friend request exists (receiver has sent to sender)
            if reversed_sent_request:
                raise ReversedFriendRequestError(receiver_info)

            # Check if they are already friends
            if already_a_friend:
                raise AlreadyAFriendError(receiver_info)

        # validated user
        if is_validated_email:
            return True

    def create(self, data: dict) -> FriendRequest:
        sender: User = data.get("Sender")
        receiver: User = data.get("Receiver")
        user_email: str = data.get("UserEmail")

        email_data: dict = {"email": user_email}

        new_friend_request = FriendRequest(sender=sender, receiver=receiver)

        if self.validate(sender=sender, data=email_data):
            new_friend_request.save()
            return new_friend_request
