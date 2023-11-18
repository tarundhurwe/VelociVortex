from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import EmailValidator

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def validate(self, data):
        required_fields = ["username", "email", "first_name", "last_name", "password"]

        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is a required field")

        return data