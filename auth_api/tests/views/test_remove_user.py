import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User


@pytest.mark.usefixtures("create_test_user")
@pytest.mark.django_db
class TestRemoveUserView:
    url = "/auth/api/v2/remove-user"

    def test_remove_user_success(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, headers=headers, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "User removed Successfully."

        user = User.objects.get(email="koushikmallik001@gmail.com")
        assert user
        assert user.is_deleted is True

    def test_remove_user_unauthorized(self, api_client: APIClient):
        headers = {
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, headers=headers, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserNotAuthenticatedError: The user is not authenticated, please re-login."
        )
