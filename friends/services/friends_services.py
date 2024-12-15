from typing import Optional

from psycopg2 import DatabaseError

from friends.friend_types.export_friend import ExportFriendList, ExportFriend
from friends.friend_types.export_friend_requests import ExportFriendRequest, ExportFriendRequestList
from friends.models.friend_model import Friend
from friends.models.friend_request_model import FriendRequest


class UseFriendServices:
    @staticmethod
    def get_all_friends_service() -> Optional[ExportFriendList]:
        try:
            friends=Friend.objects.all()
        except Exception:
            raise DatabaseError()
        if friends:
            all_friend=[]
            for friend in friends:
                export_details=ExportFriend(**friend.model_to_dict())
                all_friend.append(export_details)
            all_friend_details=ExportFriendList(friend_list=all_friend)
            return all_friend_details
        else:
            return None
    @staticmethod
    def get_all_friend_requests() -> Optional[ExportFriendRequest]:
        try:
            requests=FriendRequest.objects.all()
        except Exception:
            raise DatabaseError()
        if requests:
            friend_requests=[]
            for req in requests:
                export_requests=ExportFriendRequest(**req.model_to_dict())
                friend_requests.append(export_requests)
            all_friend_details=ExportFriendRequestList(friend_requests=friend_requests)
            return all_friend_details
        else:
            return None
