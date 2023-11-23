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

class UpdateInfoSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        # Update user fields
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Update password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance