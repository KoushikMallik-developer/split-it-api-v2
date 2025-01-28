import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from auth_api.models.user_models.user import User


@pytest.mark.django_db
class TestRefreshTokenView:
    url = "/auth/api/v2/refresh-token"

    @pytest.mark.usefixtures("create_test_user")
    def test_refresh_token_success(self, api_client: APIClient):
        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        headers = {
            "Authorization": "Bearer " + str(refresh),
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, headers=headers, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert response.data["message"] == "Refreshed access token successfully."

    def test_refresh_token_missing_token(self, api_client: APIClient):
        headers = {
            "Authorization": "Bearer ",
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, headers=headers, format="json")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            response.data["message"]
            == "The user is not authenticated, please re-login."
        )

    def test_refresh_token_invalid_token(self, api_client: APIClient):
        headers = {
            "Authorization": "Bearer " + "invalidToken",
            "Content-Type": "application/json",
        }
        response = api_client.post(self.url, headers=headers, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["message"] == "TokenError: Token is invalid or expired"
