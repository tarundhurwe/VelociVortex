from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

# Create your views here.


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": request.user.username})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateWorkHistory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"work history of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"projects of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdatePersonalLinks(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"links of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
