from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import serializers
from auth_api.services.helpers import is_valid_uuid
from friends.friend_exceptions.friend_exceptions import FriendRequestNotFoundError
from friends.models.friend_request import FriendRequest


class RemoveFriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        friend_request_id: str = data.get("friend_request_id")

        # User uuid Validation
        if not friend_request_id or not isinstance(friend_request_id, str):
            raise ValueError("User ID is required.")

        if not is_valid_uuid(value=friend_request_id):
            raise ValueError("User ID is not valid.")

        # checking the provided email is part of the friend request list
        existing_friend_request = FriendRequest.objects.filter(
            Q(sender__id=friend_request_id) | Q(receiver__id=friend_request_id)
        ).exists()

        if not existing_friend_request:
            raise FriendRequestNotFoundError()

        # validated
        return True

    def remove_friend_request(self, data: dict):
        if self.validate(data=data):
            user_id: str = data.get("primary_user_id")
            friend_request_id: str = data.get("friend_request_id")
            try:
                existing_friend_request: FriendRequest = FriendRequest.objects.get(
                    Q(sender__id=user_id, receiver__id=friend_request_id)
                    | Q(receiver__id=user_id, sender__id=friend_request_id)
                )

                existing_friend_request.delete()
            except ObjectDoesNotExist:
                raise FriendRequestNotFoundError()
