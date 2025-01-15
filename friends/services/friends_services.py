from typing import Optional

from django.db.models import Q
from psycopg2 import DatabaseError

from friends.export_types.friend_types.export_friend import (
    ExportFriendList,
    ExportFriend,
)
from friends.export_types.friend_types.export_friend_requests import (
    ExportFriendRequest,
    ExportFriendRequestList,
)
from friends.export_types.request_data_types.accept_friend_requeset import (
    AcceptFriendRequestType,
)

from friends.export_types.request_data_types.add_friend import AddFriendRequestType
from friends.export_types.request_data_types.remove_friend import RemoveFriendType
from friends.export_types.request_data_types.remove_friend_requeset import (
    RemoveFriendRequestType,
)
from friends.export_types.request_data_types.search_friend import (
    SearchFriendRequestType,
)
from friends.friend_exceptions.friend_exceptions import (
    FriendRequestNotSentError,
    FriendRequestNotAcceptedError,
)
from friends.models.friend import Friend
from friends.models.friend_request import FriendRequest
from friends.serializers.accept_friend_request_serializer import (
    AcceptFriendRequestSerializer,
)
from friends.serializers.friend_request_serializer import FriendRequestSerializer
from friends.serializers.remove_friend_request_serializer import (
    RemoveFriendRequestSerializer,
)
from friends.serializers.remove_friend_serializer import RemoveFriendSerializer


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
    def get_searched_friends(
        request_data: SearchFriendRequestType, user_id: str
    ) -> Optional[ExportFriendList]:
        friends = Friend.objects.filter(
            Q(user1__fname__icontains=request_data.keyword)
            | Q(user1__lname__icontains=request_data.keyword)
            | Q(user1__email__icontains=request_data.keyword)
            | Q(user2__fname__icontains=request_data.keyword)
            | Q(user2__lname__icontains=request_data.keyword)
            | Q(user2__email__icontains=request_data.keyword)
        )
        if friends:
            all_friend = [ExportFriend(**friend.model_to_dict()) for friend in friends]
            return ExportFriendList(friend_list=all_friend, user_id=user_id)
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
    def create_new_friend_request_service(
        request_data: AddFriendRequestType, uid: str
    ) -> dict:
        data: dict = {
            "sender": uid,
            "receiver": request_data.user_email,
        }
        friend_request = FriendRequestSerializer().create(data=data)
        if friend_request:
            return {
                "successMessage": f"Friend request sent to {request_data.user_email}",
                "errorMessage": None,
            }
        else:
            raise FriendRequestNotSentError()

    @staticmethod
    def accept_friend_request_service(
        request_data: AcceptFriendRequestType, uid: str
    ) -> dict:
        data: dict = {
            "receiver": uid,
            "sender": request_data.user_email,
        }
        friend_request = AcceptFriendRequestSerializer().create(data=data)
        if friend_request:
            return {
                "successMessage": "Friend request accepted.",
                "errorMessage": None,
            }
        else:
            raise FriendRequestNotAcceptedError()

    @staticmethod
    def remove_friend_service(request_data: RemoveFriendType, uid: str) -> dict:
        data: dict = {"user_email": request_data.user_email, "primary_user_id": uid}
        friend = RemoveFriendSerializer().remove_friend(data=data)
        if friend:
            return {
                "successMessage": "Friend removed.",
                "errorMessage": None,
            }

    @staticmethod
    def remove_friend_request_service(
        request_data: RemoveFriendRequestType, uid: str
    ) -> dict:
        data: dict = {
            "primary_user_id": uid,
            "friend_request_email": request_data.user_email,
        }
        friend_request = RemoveFriendRequestSerializer().remove_friend_request(
            data=data
        )
        if friend_request:
            return {
                "successMessage": "Friend request deleted.",
                "errorMessage": None,
            }
