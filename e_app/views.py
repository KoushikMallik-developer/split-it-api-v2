from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, _):
        return Response(
            data={"data": "Test Successful", "errorMessage": None},
            status=status.HTTP_200_OK,
            content_type="application/json",
        )
