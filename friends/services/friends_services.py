from typing import Optional

from django.db.models import Q
from psycopg2 import DatabaseError

from auth_api.models.user_models.user import User
from friends.export_types.friend_types.export_friend import (
    ExportFriendList,
    ExportFriend,
)
from friends.export_types.friend_types.export_friend_requests import (
    ExportFriendRequest,
    ExportFriendRequestList,
)

from friends.export_types.request_data_types.add_friend import AddFriendRequestType
from friends.friend_exceptions.friend_exceptions import FriendRequestNotSentError
from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest
from friends.serializers.friend_serializer import FriendSerializer


class UseFriendServices:
    @staticmethod
    def get_all_friends_service(user_id: str) -> Optional[ExportFriendList]:
        try:
            friends = Friend.objects.filter(Q(user1__id=user_id) | Q(user2__id=user_id))
        except Exception:
            raise DatabaseError()
        if friends:
            all_friend = []
            for friend in friends:
                export_details = ExportFriend(**friend.model_to_dict())
                all_friend.append(export_details)
            all_friend_details = ExportFriendList(
                friend_list=all_friend, user_id=user_id
            )
            return all_friend_details
        else:
            return None

    @staticmethod
    def get_all_friend_requests(user_id: str) -> Optional[ExportFriendRequest]:
        try:
            requests = FriendRequest.objects.filter(
                Q(sender__id=user_id) | Q(receiver__id=user_id)
            )
        except Exception:
            raise DatabaseError()
        if requests:
            friend_requests = []
            for req in requests:
                export_requests = ExportFriendRequest(**req.model_to_dict())
                friend_requests.append(export_requests)
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests
            )
            return all_friend_details
        else:
            return None

    @staticmethod
    def get_all_sent_friend_requests(user_id: str) -> Optional[ExportFriendRequest]:
        try:
            requests = FriendRequest.objects.filter(Q(sender__id=user_id))
        except Exception:
            raise DatabaseError()
        if requests:
            friend_requests = []
            for req in requests:
                export_requests = ExportFriendRequest(**req.model_to_dict())
                friend_requests.append(export_requests)
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests, user_id=user_id
            )
            return all_friend_details
        else:
            return None

    @staticmethod
    def get_all_received_friend_requests(user_id: str) -> Optional[ExportFriendRequest]:
        try:
            requests = FriendRequest.objects.filter(Q(receiver__id=user_id))
        except Exception:
            raise DatabaseError()
        if requests:
            friend_requests = []
            for req in requests:
                export_requests = ExportFriendRequest(**req.model_to_dict())
                friend_requests.append(export_requests)
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests, user_id=user_id
            )
            return all_friend_details
        else:
            return None

    @staticmethod
    def save_friend_request(sender: User, receiver: User) -> FriendRequest:
        new_friend_request = FriendRequest(sender=sender, receiver=receiver)
        new_friend_request.save()
        return new_friend_request

    @staticmethod
    def create_new_friend_request_service(
        request_data: AddFriendRequestType, uid: str
    ) -> dict:
        is_validate_request: bool = FriendSerializer().validate(
            data=request_data.model_dump()
        )
        if is_validate_request:
            # Retrieve sender and receiver
            receiver: User = User.objects.get(email=request_data.user_email)
            sender: User = User.objects.get(id=uid)

            # Save the friend request
            UseFriendServices().save_friend_request(sender=sender, receiver=receiver)

            return {
                "successMessage": f"Friend request sent to {receiver.username.upper() if receiver.username else receiver.email}",
                "errorMessage": None,
            }
        else:
            raise FriendRequestNotSentError()
