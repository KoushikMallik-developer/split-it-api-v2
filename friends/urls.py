from django.urls import path

from auth_api.views.all_users import AllUsersView
from auth_api.views.create_user import CreateUsersView
from auth_api.views.otp_view import SendOTPView
from auth_api.views.password_reset import PasswordResetView
from auth_api.views.remove_user import RemoveUserView
from auth_api.views.sign_in import SignInView
from auth_api.views.update_password import UpdatePasswordView
from auth_api.views.update_profile import UpdateProfileView
from auth_api.views.user_details import UserDetailView
from auth_api.views.validate_otp_view import ValidateOTPView
from friends.views.all_friend_requests import AllFriendRequestsView
from friends.views.all_friends import AllFriendsView

urlpatterns = [
    path("friends", AllFriendsView.as_view(), name="All-Friends"),
    path("friend-requests", AllFriendRequestsView.as_view(), name="All-Friend-Requests"),
]
