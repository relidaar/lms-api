from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


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
        fields = ('uuid', 'full_name', 'email', 'password')
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(ModelSerializer):
    """Custom update serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ('uuid', 'full_name', 'email',)
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
        }
