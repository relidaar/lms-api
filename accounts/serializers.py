from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import UserRoles


class CustomLoginSerializer(LoginSerializer):
    """Custom login serializer for dj-rest-auth."""
    username = None
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(ModelSerializer):
    """Custom serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ('uid', 'full_name', 'email', 'password', 'role')
        extra_kwargs = {
            'uid': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.role = role

        if role is UserRoles.ADMIN:
            user.is_staff = True
            user.is_superuser = True

        user.save()
        return user


class UserUpdateSerializer(ModelSerializer):
    """Custom update serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ('uid', 'full_name', 'email',)
        extra_kwargs = {
            'uid': {
                'read_only': True,
            },
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        return instance
