from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserProfileDetailSerializer
from .models import UserProfile

# Create your views here.


class UpdateProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Method to handle the creation of new data for user's description and profile picture.
        """
        try:
            user = request.user
            # adding user id
            data = {"user": user.id}
            data.update(request.data)
            serializer = UserProfileDetailSerializer(data=data)
            
            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Method to handle the updation of the user's description and profile picture.
        """
        try:
            try:
                user = User.objects.get(username=request.user.username)
                user = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserProfileDetailSerializer(
                user, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            user_name = request.user.username
            updated_data = {"username": user_name}
            updated_data.update(serializer.data)
            return Response(updated_data, status=status.HTTP_200_OK)
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
