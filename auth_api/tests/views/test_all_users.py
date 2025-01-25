import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAllUsersView:
    @pytest.mark.usefixtures("create_test_user")
    def test_get_all_users(self):
        client = APIClient()
        url = "/auth/api/v2/all-users"
        response = client.get(url, None, format="json")

        assert response
        assert response.status_code == 200
        assert response.content_type == "application/json"
        response_data = response.data

        assert "data" in response_data
        assert "message" in response_data
        assert not response_data["message"]
        assert isinstance(response_data["data"], dict)

        assert "user_list" in response_data["data"]
        user_list = response_data["data"]["user_list"]
        assert isinstance(user_list, list)

        for user in user_list:
            assert "email" in user
            assert "fname" in user
            assert "lname" in user
            assert "dob" in user
            assert "phone" in user
            assert user["email"] and isinstance(user["email"], str)
            assert user["fname"] and isinstance(user["fname"], str)
            assert user["lname"] and isinstance(user["lname"], str)
            assert user["dob"] is None or isinstance(user["dob"], str)
            assert user["phone"] is None or isinstance(user["phone"], str)

    @pytest.mark.usefixtures("empty_database")
    def test_empty_user_list(self):
        client = APIClient()
        url = "http://localhost:8000/auth/api/v2/all-users"
        response = client.get(url, None, format="json")

        assert response
        assert response.status_code == 200
        assert response.content_type == "application/json"
        response_data = response.data
        assert "data" in response_data
        assert isinstance(response_data["data"], dict)
        assert "user_list" in response_data["data"]
        assert isinstance(response_data["data"]["user_list"], list)
        assert len(response_data["data"]["user_list"]) == 0
