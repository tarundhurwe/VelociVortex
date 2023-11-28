from rest_framework import serializers
from .models import UserProfile, WorkHistory, Project, PersonalLink, Skill


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "profile_picture", "current_title", "description"]


class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = ["user", "company_name", "title", "start_date", "end_date"]


class UpdateWorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = ["work_id", "user", "company_name", "title", "start_date", "end_date"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["user", "title", "description", "link", "image"]


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_id", "user", "title", "description", "link", "image"]


class PersonalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalLink
        fields = ["user", "website", "link"]


class UpdatePersonalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalLink
        fields = ["link_id", "user", "website", "link"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["user", "skill", "level"]


class UpdateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["skill_id", "skill", "level"]
