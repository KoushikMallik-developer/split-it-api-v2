from django.urls import path

from friends.views.all_friend_requests import AllFriendRequestsView
from friends.views.all_friends import AllFriendsView
from friends.views.my_received_friend_requests import MyReceivedFriendRequestsView
from friends.views.my_sent_friend_requests import MySentFriendRequestsView
from friends.views.add_friend import AddFriend

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
        "add-friend",
        AddFriend.as_view(),
        name="All-Received-Requests",
    ),
]
