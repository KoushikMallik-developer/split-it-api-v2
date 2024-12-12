import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EnvRead(APIView):
    def get(self, _):
        load_dotenv()
        default_data = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USERNAME"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        }
        return Response(
            data={"data": default_data, "errorMessage": None},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
