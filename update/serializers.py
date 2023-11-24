from rest_framework import serializers
from .models import UserProfile


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "profile_picture", "current_title", "description"]

