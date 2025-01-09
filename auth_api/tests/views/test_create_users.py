import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User
from auth_api.services.definitions import DEFAULT_VERIFICATION_MESSAGE


@pytest.mark.django_db
class TestCreateUsersView:
    url = "/auth/api/v2/create-users"

    def test_create_user_success(self):
        client = APIClient()
        data = {
            "email": "testuser@example.com",
            "password": "TestPassword123",
            "fname": "Test",
            "lname": "User",
        }
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == DEFAULT_VERIFICATION_MESSAGE

        user = User.objects.get(email="testuser@example.com")
        assert user.fname == "Test"
        assert user.lname == "User"

    def test_create_user_missing_name_fields(self):
        client = APIClient()
        data = {"email": "testuser@example.com", "password": "TestPassword123"}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data

    def test_create_user_missing_email_fields(self):
        client = APIClient()
        data = {"email": "testuser@example.com", "fname": "John", "lname": "Doe"}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data

    def test_create_user_missing_password_fields(self):
        client = APIClient()
        data = {"fname": "John", "lname": "Doe", "password": "TestPassword123"}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data

    def test_create_user_invalid_email(self):
        client = APIClient()
        data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "TestPassword123",
            "fname": "Test",
            "lname": "User",
            "dob": "1990-01-01",
            "phone": "1234567890",
        }
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data

    def test_create_user_duplicate_email(self):
        client = APIClient()
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "TestPassword123",
            "fname": "Test",
            "lname": "User",
            "dob": "1990-01-01",
            "phone": "1234567890",
        }
        client.post(self.url, data, format="json")  # Create the first user

        response = client.post(
            self.url, data, format="json"
        )  # Attempt to create a duplicate user

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "message" in response.data
