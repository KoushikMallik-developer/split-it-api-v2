import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User

@pytest.mark.django_db
class TestUpdatePasswordView:
    url = "/auth/api/v2/update-password"

    @pytest.mark.usefixtures("create_test_user")
    def test_update_password_success(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        data = {
            "password1": "123456",
            "password2": "123456",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["successMessage"] == "Password updated successfully."
        assert response.data["errorMessage"] is None

    def test_update_password_unauthorized(self, api_client: APIClient):
        data = {
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["errorMessage"] == "UserNotAuthenticatedError: The user is not authenticated, please re-login."
        assert response.data["successMessage"] is None

    @pytest.mark.usefixtures("create_test_user")
    def test_update_password_not_matching(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        data = {
            "password1": "newpassword123",
            "password2": "differentpassword",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["errorMessage"] == "PasswordNotMatchError: Passwords are not matching or not in correct format."
        assert response.data["successMessage"] is None

    @pytest.mark.usefixtures("create_test_user")
    def test_update_password_invalid_data(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        data = {
            "password1": "newpassword123",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data["errorMessage"] == "ValueError: Please provide both the passwords."
        assert response.data["successMessage"] is None
