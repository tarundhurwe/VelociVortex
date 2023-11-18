from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
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
                if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                    return Response({"error": "User with same email or same username already exists."}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_created)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user_name = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=user_name, password=password)

            if user:
                refresh_token = RefreshToken.for_user(user)
                access_token = str(refresh_token.access_token)

                return Response({"access_token": access_token}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        

