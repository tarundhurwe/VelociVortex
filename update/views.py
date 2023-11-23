from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserProfileDetailSerializer

# Create your views here.


class UpdateProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = UserProfileDetailSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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
