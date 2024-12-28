from django.urls import path

from friends.views.accept_friend_request import AcceptFriendRequest
from friends.views.all_friend_requests import AllFriendRequestsView
from friends.views.all_friends import AllFriendsView
from friends.views.my_received_friend_requests import MyReceivedFriendRequestsView
from friends.views.my_sent_friend_requests import MySentFriendRequestsView
from friends.views.add_friend import AddFriend
from friends.views.remove_friend_request import RemoveFriendRequest

urlpatterns = [
    path("my-friends", AllFriendsView.as_view(), name="All-Friends"),
    path(
        "my-friend-requests",
        AllFriendRequestsView.as_view(),
        name="All-Friend-Requests",
    ),
    path(
        "my-sent-friend-requests",
        MySentFriendRequestsView.as_view(),
        name="All-Sent-Requests",
    ),
    path(
        "my-received-friend-requests",
        MyReceivedFriendRequestsView.as_view(),
        name="All-Received-Requests",
    ),
    path(
        "send-friend-request",
        AddFriend.as_view(),
        name="Add-Friends",
    ),
    path(
        "accept-friend",
        AcceptFriendRequest.as_view(),
        name="Accept-Friends",
    ),
    path(
        "remove-friend-request",
        RemoveFriendRequest.as_view(),
        name="Remove-Friend-Request",
    ),
]
