from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import StudentProfile, InstructorProfile, UserProfile


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
        fields = ('uuid', 'full_name', 'email', 'password',
                  'is_staff', 'is_active', 'groups',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups_data)
        user.save()
        return user


class UserUpdateSerializer(ModelSerializer):
    """Custom update serializer for user model."""

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'full_name', 'email', 'groups',)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get(
            'full_name', instance.full_name)
        instance.groups.set(validated_data.get('groups', instance.groups))
        instance.save()
        return instance


class GroupSerializer(ModelSerializer):
    """Custom serializer for group model."""

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(ModelSerializer):
    """Custom serializer for permission model."""

    class Meta:
        model = Permission
        fields = '__all__'


class UserProfileSerializer(ModelSerializer):
    """Custom serializer for user profile model."""
    user = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        abstract = True
        fields = ('uuid', 'user', 'created_date', 'modified_date',)


class StudentProfileSerializer(UserProfileSerializer):
    """Custom serializer for student profile model."""

    class Meta:
        model = StudentProfile
        fields = UserProfileSerializer.Meta.fields + ()


class InstructorProfileSerializer(UserProfileSerializer):
    """Custom serializer for instructor profile model."""

    class Meta:
        model = InstructorProfile
        fields = UserProfileSerializer.Meta.fields + ()
