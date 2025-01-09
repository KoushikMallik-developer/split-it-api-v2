import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User


@pytest.mark.usefixtures("create_test_user")
@pytest.mark.django_db
class TestRemoveUserView:
    url = "/auth/api/v2/remove-user"

    def test_remove_user_success(self, api_client: APIClient, access_token: str):
        data = {"email": "koushikmallik001@gmail.com"}
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "User removed Successfully."

        with pytest.raises(User.DoesNotExist):
            User.objects.get(email="koushikmallik001@gmail.com")

    def test_remove_user_not_found(self, api_client: APIClient, access_token: str):
        data = {"email": "nonexistentuser@example.com"}
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserNotFoundError: This user is not registered. Please register as new user."
        )

    def test_remove_user_missing_email(self, api_client: APIClient, access_token: str):
        data = {}
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data["message"] == "ValueError: Email is required."

    def test_remove_user_unauthorized(self, api_client: APIClient):
        data = {"email": "koushikmallik001@gmail.com"}
        headers = {
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserNotAuthenticatedError: The user is not authenticated, please re-login."
        )
