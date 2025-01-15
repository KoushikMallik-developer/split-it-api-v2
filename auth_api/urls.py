from django.urls import path

from auth_api.views.all_users import AllUsersView
from auth_api.views.create_user import CreateUsersView
from auth_api.views.otp_view import SendOTPView
from auth_api.views.password_reset import PasswordResetView
from auth_api.views.refresh_token import RefreshTokenView
from auth_api.views.remove_user import RemoveUserView
from auth_api.views.sign_in import SignInView
from auth_api.views.update_password import UpdatePasswordView
from auth_api.views.update_profile import UpdateProfileView
from auth_api.views.user_details import UserDetailView
from auth_api.views.validate_otp_view import ValidateOTPView

urlpatterns = [
    path("create-users", CreateUsersView.as_view(), name="Create-Users"),
    path("sign-in", SignInView.as_view(), name="user-sign-in"),
    path("update-profile", UpdateProfileView.as_view(), name="Update-User-profile"),
    path("user-details", UserDetailView.as_view(), name="user-details"),
    path("all-users", AllUsersView.as_view(), name="All-Users"),
    path("remove-user", RemoveUserView.as_view(), name="Remove-User"),
    path("send-otp", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp", ValidateOTPView.as_view(), name="verify-otp"),
    path(
        "reset-password",
        PasswordResetView.as_view(),
        name="send-reset-password-email",
    ),
    path("update-password", UpdatePasswordView.as_view(), name="Change-User-Password"),
    path("refresh-token", RefreshTokenView.as_view(), name="refresh-token"),
    # path("clear-caches", ClearServerCaches.as_view(), name="clear-caches"),
]
