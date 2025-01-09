from unittest.mock import patch

import pytest
from rest_framework import status

from auth_api.models.user_models.user import User
from auth_api.services.otp_services.otp_services import OTPServices
from rest_framework.test import APIClient


@pytest.mark.django_db
@pytest.mark.usefixtures("create_test_user")
class TestVerifyOTPView:
    url = "/auth/api/v2/verify-otp"

    def test_verify_otp_success(self, api_client: APIClient):
        User.objects.create(email="testuser001@example.com", is_active=False)
        with patch.object(OTPServices, "verify_otp", return_value=True):
            data = {"email": "testuser001@example.com", "otp": "123456"}
            response = api_client.post(self.url, data, format="json")

            assert response.status_code == status.HTTP_200_OK
            assert response.data["token"]
            assert isinstance(response.data["token"], dict)
            assert response.data["token"]["access"]
            assert isinstance(response.data["token"]["access"], str)
            assert response.data["message"] is None

    def test_verify_otp_failure_with_invalid_email(self, api_client: APIClient):
        with patch.object(OTPServices, "verify_otp", return_value=False):
            data = {"email": "invalid_email@example.com", "otp": "123456"}
            response = api_client.post(self.url, data, format="json")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert (
                response.data["message"]
                == "UserNotFoundError: This user is not registered. Please register as new user."
            )

    def test_verify_otp_failure_with_invalid_otp(self, api_client: APIClient):
        User.objects.create(email="testuser001@example.com", is_active=False)
        with patch.object(OTPServices, "verify_otp", return_value=False):
            data = {"email": "testuser001@example.com", "otp": "123456"}
            response = api_client.post(self.url, data, format="json")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.data["message"] == "OTPNotVerifiedError: OTP did not match."
