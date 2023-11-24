from rest_framework import serializers
from .models import UserProfile


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_picture", "description", "current_title"]
