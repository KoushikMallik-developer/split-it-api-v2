import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestPasswordResetView:
    url = "/auth/api/v2/reset-password"

    @pytest.mark.usefixtures("create_test_user")
    def test_password_reset_success(self, api_client: APIClient):
        data = {"email": "koushikmallik001@gmail.com"}
        response = api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password reset email sent successfully."

    def test_password_reset_user_not_found(self, api_client: APIClient):
        data = {"email": "nonexistentuser@example.com"}
        response = api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserNotFoundError: This user is not registered. Please register as new user."
        )

    def test_password_reset_missing_email(self, api_client: APIClient):
        data = {}
        response = api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserNotFoundError: This user is not registered. Please register as new user."
        )
