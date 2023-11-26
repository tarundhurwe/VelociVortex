from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import (
    UserProfileDetailSerializer,
    WorkHistorySerializer,
    UpdateWorkHistorySerializer,
    ProjectSerializer,
    UpdateProjectSerializer,
)
from .models import UserProfile, WorkHistory, Project
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
            # to ensure that the user is able to update their own profiles only
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

    # add new work history
    def post(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Api to add new work history to the profile.
        """
        try:
            validate_data = ValidateData()
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")

            date_validation = validate_data.verify_start_and_end_dates(
                start_date, end_date
            )
            work_history = WorkHistory.objects.filter(user=request.user)

            if (
                not end_date
                and validate_data.check_for_present_company(work_history) > 0
            ):
                return Response(
                    {"error": "Only one work history can have end date as present."},
                    status=status.HTTP_400_BAD_REQUEST,
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

    # update existing work history
    def put(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Api to handle the updation of work history.
        """
        try:
            validate_data = ValidateData()
            work_id = request.data.get("work_id")
            if not work_id:
                return Response(
                    {"error": "Can not update work history without the id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get(username=request.user.username)
            try:
                work = WorkHistory.objects.get(work_id=work_id, user=user)
            except WorkHistory.DoesNotExist:
                return Response(
                    {"error": "work associated with the user does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # checks before updates
            start_date = request.data.get("start_date")
            end_date = request.data.get("end_date")
            if start_date and end_date and len(end_date) == 10:
                date_validation = validate_data.verify_start_and_end_dates(
                    start_date, end_date
                )
                if not isinstance(date_validation, bool):
                    return Response(
                        {"error": date_validation}, status=status.HTTP_400_BAD_REQUEST
                    )

            # user should not be allowed to add more than one company as present company
            elif start_date and end_date == "":
                work_history = WorkHistory.objects.filter(user=request.user)

                if (
                    not end_date
                    and validate_data.check_for_present_company(work_history) > 0
                ):
                    return Response(
                        {
                            "error": "Only one work history can have end date as present."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # user should not be allowed to update end date as date before the start date
            elif not start_date and end_date:
                start_date = str(work.start_date)
                date_validation = validate_data.verify_start_and_end_dates(
                    start_date, end_date
                )
                if not isinstance(date_validation, bool):
                    return Response(
                        {"error": date_validation}, status=status.HTTP_400_BAD_REQUEST
                    )

            # user should not be allowed to update start date as date date after the end date
            elif start_date and not end_date:
                if work.end_date is not None:
                    end_date = str(work.end_date)
                    date_validation = validate_data.verify_start_and_end_dates(
                        start_date, end_date
                    )
                    if not isinstance(date_validation, bool):
                        return Response(
                            {"error": date_validation},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            serializer = UpdateWorkHistorySerializer(
                work, data=request.data, partial=True
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

    # delete work history
    def delete(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Api to handle deletion of the work history.
        """
        try:
            work_id = request.data.get("work_id")
            if not work_id:
                return Response(
                    {"error": "Can not delete the work history without the id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                work = WorkHistory.objects.get(work_id=work_id, user=request.user)
            except WorkHistory.DoesNotExist:
                return Response(
                    {"error": "work history does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            work.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateProject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Method to handle the addition of new project in the user's profile.
        """
        try:
            user = User.objects.get(username=request.user.username)
            data = request.data
            data["user"] = user

            serializer = ProjectSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            project = serializer.save()
            project_data = serializer.data
            project_data["project_id"] = project.project_id
            return Response(project_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Method to handle the updation of a project in user's profile.
        """
        try:
            project_id = request.data.get("project_id")
            if not project_id:
                return Response(
                    {"error": "Can not update project without the id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data
            user = User.objects.get(username=request.user.username)
            data["user"] = user

            try:
                project = Project.objects.get(user=user, project_id=project_id)
            except Project.DoesNotExist:
                return Response(
                    {"error": "Project does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UpdateProjectSerializer(project, data=data, partial=True)

            if not serializer.is_valid():
                return Response(
                    {"error": f"{serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            project = serializer.save()
            project_data = serializer.data
            project_data["project_id"] = project.project_id
            return Response(project_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """
        @author: Tarun https://github.com/tarundhurwe
        :method description: Method to handle the deletion of a project in user's profile.
        """
        try:
            project_id = request.data.get("project_id")
            if not project_id:
                return Response(
                    {"error": "Can not update project without the id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = User.objects.get(username=request.user.username)
            try:
                project = Project.objects.get(project_id=project_id, user=user)
            except Project.DoesNotExist:
                return Response(
                    {"error": "Project does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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
