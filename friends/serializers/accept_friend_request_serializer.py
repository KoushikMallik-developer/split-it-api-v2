from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import (
    UserNotFoundError,
    UserNotAuthenticatedError,
)
from auth_api.models.user_models.user import User
from auth_api.services.helpers import (
    is_valid_uuid,
    validate_user_uid,
)
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
            if not is_valid_uuid(value=data.get("sender")):
                raise ValueError("User ID is not valid.")

            if not validate_user_uid(uid=data.get("sender")).is_validated:
                raise UserNotFoundError(msg="This user is not registered with us.")
        else:
            raise ValueError("User ID is required.")

        sender: User = User.objects.get(id=data.get("sender"))

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
                sender: User = User.objects.get(id=data.get("sender"))
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
