import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User


@pytest.mark.django_db
class TestUpdateProfileView:
    url = "/auth/api/v2/update-profile"

    @pytest.mark.usefixtures("create_test_user")
    def test_update_profile_success(self, api_client: APIClient, access_token: str):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        data = {
            "fname": "NewFirstName",
            "lname": "NewLastName",
            "email": "koushikmallik001@gmail.com",
            "username": "koushikmallik",
            "password": "1234567",
            "image": "/images/users/defaultUserImage.png",
            "dob": "1998-01-01",
            "phone": "1234567890",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "User details updated Successfully."

        user = User.objects.get(email="koushikmallik001@gmail.com")
        assert user.fname == "NewFirstName"
        assert user.lname == "NewLastName"

    def test_update_profile_unauthorized(self, api_client: APIClient):
        data = {
            "username": "newusername",
            "fname": "NewFirstName",
            "lname": "NewLastName",
        }
        response = api_client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            response.data["message"]
            == "UserNotAuthenticatedError: The user is not authenticated, please re-login."
        )

    @pytest.mark.usefixtures("create_test_user")
    def test_update_profile_invalid_data(
        self, api_client: APIClient, access_token: str
    ):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
        }
        data = {
            "fname": "NewFirstName9",
            "lname": "NewLastName",
        }
        response = api_client.post(self.url, data, headers=headers, format="json")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            response.data["message"]
            == "ValueError: First name is not in correct format."
        )
