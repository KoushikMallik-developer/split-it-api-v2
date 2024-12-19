from django.urls import path

from friends.views.all_friend_requests import AllFriendRequestsView
from friends.views.all_friends import AllFriendsView

urlpatterns = [
    path("my-friends", AllFriendsView.as_view(), name="All-Friends"),
    path(
        "my-friend-requests",
        AllFriendRequestsView.as_view(),
        name="All-Friend-Requests",
    ),
]
