import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EnvRead(APIView):
    def get(self, _):
        load_dotenv()
        return Response(
            data={"data": None, "errorMessage": None},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
