from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserProfileDetailSerializer, WorkHistorySerializer
from .models import UserProfile, WorkHistory
from .validation import ValidateData

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
            data = request.data
            data["user"] = user.id
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
                return Response(
                    {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
                )

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Api to add new work history to the profile.
        """
        try:
            validate_instance = ValidateData()
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
            date_validation = validate_instance.verify_start_and_end_dates(
                start_date, end_date
            )
            if not isinstance(date_validation, bool):
                return Response(
                    {"error": date_validation}, status=status.HTTP_400_BAD_REQUEST
                )
            user = request.user
            data = request.data
            data["user"] = user.id
            serializer = WorkHistorySerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            work = serializer.save()
            work_data = serializer.data
            work_data["work_id"] = work.work_id
            return Response(work_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self):
        pass


class UpdateProject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"projects of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdatePersonalLinks(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"links of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateSkills(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            return Response({"working": f"skills of {request.user.username}"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )