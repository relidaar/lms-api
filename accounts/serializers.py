from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from accounts.models import StudentProfile, InstructorProfile
from common.serializers import UUIDHyperlinkedRelatedField


class CustomLoginSerializer(LoginSerializer):
    """Custom login serializer for dj-rest-auth."""
    username = None
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Custom serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ('url', 'uuid', 'full_name', 'email', 'password',
                  'is_staff', 'is_active', 'groups',)
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'view_name': 'user-detail', 'lookup_field': 'uuid', },
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups_data)
        user.save()
        return user


class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """Custom update serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ('url', 'uuid', 'full_name', 'email', 'groups',)
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'uuid', },
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.full_name = validated_data.get(
            'full_name', instance.full_name)
        instance.groups.set(validated_data.get('groups', instance.groups))
        instance.save()
        return instance


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Custom serializer for group model."""
    permissions = serializers.HyperlinkedRelatedField(
        view_name='permission-detail',
        queryset=Permission.objects.all(),
        many=True,
    )

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    """Custom serializer for permission model."""

    class Meta:
        model = Permission
        fields = ('url', 'name', 'codename',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Custom serializer for user profile model."""
    user = UUIDHyperlinkedRelatedField(
        view_name='user-detail',
        queryset=get_user_model().objects.all(),
    )

    class Meta:
        abstract = True
        fields = ('url', 'uuid', 'user', 'created_date', 'modified_date',)


class StudentProfileSerializer(UserProfileSerializer):
    """Custom serializer for student profile model."""
    class Meta:
        model = StudentProfile
        fields = UserProfileSerializer.Meta.fields + ()
        extra_kwargs = {
            'url': {'view_name': 'student-detail', 'lookup_field': 'uuid', },
        }


class InstructorProfileSerializer(UserProfileSerializer):
    """Custom serializer for instructor profile model."""
    class Meta:
        model = InstructorProfile
        fields = UserProfileSerializer.Meta.fields + ()
        extra_kwargs = {
            'url': {'view_name': 'instructor-detail', 'lookup_field': 'uuid', },
        }
