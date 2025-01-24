from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from psycopg2 import DatabaseError

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.user_types.export_user import ExportUser, ExportUserList
from auth_api.models.user_models.user import User
from auth_api.services.helpers import validate_email_format
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
)
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
    def get_all_friends_service(user_id: str) -> Optional[list]:
        try:
            friends = User.objects.get(id=user_id).friends.all()
        except Exception:
            raise DatabaseError()
        if friends:
            all_friends = ExportUserList(
                user_list=[ExportUser(**friend.model_to_dict()) for friend in friends]
            )
            return all_friends.model_dump().get("user_list")
        else:
            return None

    @staticmethod
    def get_searched_friends(
        request_data: SearchFriendRequestType, user_id: str
    ) -> Optional[list]:
        try:
            user: User = User.objects.get(id=user_id)
            if validate_email_format(request_data.keyword):
                friends = user.friends.filter(email=request_data.keyword)

            else:
                keywords = request_data.keyword.split(" ")
                query = Q()
                for keyword in keywords:
                    query |= Q(fname__icontains=keyword) | Q(lname__icontains=keyword)
                friends = user.friends.filter(query)

            if friends:
                all_friends = [
                    ExportUser(**friend.model_to_dict()) for friend in friends
                ]
                return (
                    ExportUserList(friend_list=all_friends, user_id=user_id)
                    .model_dump()
                    .get("friend_list")
                )
            else:
                return None
        except ObjectDoesNotExist:
            raise UserNotFoundError(msg="This user is not registered with us.")

    @staticmethod
    def get_all_friend_requests(user_id: str) -> Optional[List[dict]]:
        try:
            friend_requests = FriendRequest.objects.filter(
                Q(sender__id=user_id) | Q(receiver__id=user_id)
            )
        except Exception:
            raise DatabaseError()
        if friend_requests:
            friend_requests = [
                ExportFriendRequest(**friend_request.model_to_dict())
                for friend_request in friend_requests
            ]
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests
            )
            return all_friend_details.model_dump().get("friend_requests")
        else:
            return None

    @staticmethod
    def get_all_sent_friend_requests(user_id: str) -> Optional[ExportFriendRequest]:
        try:
            friend_requests = FriendRequest.objects.filter(Q(sender__id=user_id))
        except Exception:
            raise DatabaseError()
        if friend_requests:
            friend_requests = [
                ExportFriendRequest(**friend_request.model_to_dict())
                for friend_request in friend_requests
            ]
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests
            )
            return all_friend_details.model_dump().get("friend_requests")
        else:
            return None

    @staticmethod
    def get_all_received_friend_requests(user_id: str) -> Optional[ExportFriendRequest]:
        try:
            friend_requests = FriendRequest.objects.filter(Q(receiver__id=user_id))
        except Exception:
            raise DatabaseError()
        if friend_requests:
            friend_requests = [
                ExportFriendRequest(**friend_request.model_to_dict())
                for friend_request in friend_requests
            ]
            all_friend_details = ExportFriendRequestList(
                friend_requests=friend_requests
            )
            return all_friend_details.model_dump().get("friend_requests")
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
                "message": f"Friend request sent to {request_data.user_email}",
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
        AcceptFriendRequestSerializer().create(data=data)
        return {
            "message": "Friend request accepted.",
        }

    @staticmethod
    def remove_friend_service(request_data: RemoveFriendType, uid: str) -> dict:
        data: dict = {"user_email": request_data.user_email, "primary_user_id": uid}
        RemoveFriendSerializer().remove_friend(data=data)
        return {
            "message": "Friend successfully removed.",
        }

    @staticmethod
    def remove_friend_request_service(
        request_data: RemoveFriendRequestType, uid: str
    ) -> dict:
        data: dict = {
            "primary_user_id": uid,
            "friend_request_email": request_data.user_email,
        }
        RemoveFriendRequestSerializer().remove_friend_request(data=data)
        return {
            "message": "Friend request deleted.",
        }
