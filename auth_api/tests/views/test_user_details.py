from uuid import UUID

import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestUserDetailsView:
    url = "/auth/api/v2/user-details"

    @pytest.mark.usefixtures("create_test_user")
    def test_user_details_success(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        response = api_client.get(self.url, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "User details fetched successfully."

        assert response.data["data"]["email"]
        assert isinstance(response.data["data"]["email"], str)
        assert response.data["data"]["email"] == "koushikmallik001@gmail.com"

        assert response.data["data"]["id"]
        assert isinstance(response.data["data"]["id"], UUID)

        assert response.data["data"]["is_active"] is True

        assert response.data["data"]["image"]
        assert isinstance(response.data["data"]["image"], str)

        assert response.data["data"]["fname"]
        assert isinstance(response.data["data"]["fname"], str)
        assert response.data["data"]["fname"] == "Koushik"

        assert response.data["data"]["lname"]
        assert isinstance(response.data["data"]["lname"], str)
        assert response.data["data"]["lname"] == "Google"

    def test_user_details_invalid_token(self, api_client: APIClient):
        headers = {
            "Authorization": "Bearer " + "invalid_token",
            "Content-Type": "application/json",
        }
        response = api_client.get(self.url, headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["message"] == "TokenError: Token is invalid or expired"

    def test_user_details_unauthorized(self, api_client: APIClient):
        headers = {
            "Content-Type": "application/json",
        }
        response = api_client.get(self.url, headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserNotAuthenticatedError: The user is not authenticated, please re-login."
        )
