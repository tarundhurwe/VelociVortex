from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UpdateInfoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegistationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user_name = serializer.validated_data.get("username")
                email = serializer.validated_data.get("email")
                if (
                    User.objects.filter(username=user_name).exists()
                    or User.objects.filter(email=email).exists()
                ):
                    return Response(
                        {
                            "error": "User with same email or same username already exists."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            if not request.user.is_authenticated:
                return Response(
                    {"error": "Authentication required for password update"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer = UpdateInfoSerializer(
                request.user, data=request.data, partial=True
            )
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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_name = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=user_name, password=password)

            if user:
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                refresh_token = str(token)
                return Response(
                    {"access_token": access_token, "refresh_token": refresh_token},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            refresh_token = str(token)
            return Response(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )