from django.urls import path

from friends.views.all_friend_requests import AllFriendRequestsView
from friends.views.all_friends import AllFriendsView

urlpatterns = [
    path("friends", AllFriendsView.as_view(), name="All-Friends"),
    path("friend-requests", AllFriendRequestsView.as_view(), name="All-Friend-Requests"),
]
