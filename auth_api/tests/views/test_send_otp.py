from unittest.mock import patch

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from auth_api.models.user_models.user import User
from auth_api.services.otp_services.otp_services import OTPServices


@pytest.mark.django_db
@pytest.mark.usefixtures("create_test_user")
class TestSendOTPView:
    url = "/auth/api/v2/send-otp"

    def test_send_otp_success(self):
        User.objects.create(email="testuser001@example.com", is_active=False)
        with patch.object(OTPServices, "send_otp_to_user", return_value="OK"):
            client = APIClient()
            data = {"email": "testuser001@example.com"}
            response = client.post(self.url, data, format="json")

            assert response.status_code == status.HTTP_200_OK
            assert (
                response.data["message"]
                == "Verification Email has been sent successfully to the user. Please verify your email to access the account."
            )

    def test_send_otp_user_already_verified(self):
        User.objects.create(email="testuser@example.com", is_active=True)

        client = APIClient()
        data = {"email": "testuser@example.com"}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserAlreadyVerifiedError: This user is already verified."
        )

    def test_send_otp_email_not_sent(self):
        User.objects.create(email="testuser@example.com", is_active=False)
        with patch.object(OTPServices, "send_otp_to_user", return_value="ERROR"):

            client = APIClient()
            data = {"email": "testuser@example.com"}
            response = client.post(self.url, data, format="json")

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert (
                response.data["message"]
                == "EmailNotSentError: Verification Email could not be sent."
            )

    def test_send_otp_user_not_found(self):
        client = APIClient()
        data = {"email": "nonexistentuser@example.com"}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserNotFoundError: This user is not registered. Please register as new user."
        )

    def test_send_otp_value_error(self):
        client = APIClient()
        data = {"email": ""}
        response = client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["message"]
            == "UserNotFoundError: This user is not registered. Please register as new user."
        )
