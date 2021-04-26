from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from accounts.models import StudentProfile, InstructorProfile
from accounts.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PermissionSerializer, \
    StudentProfileSerializer, InstructorProfileSerializer
from config.views import MultiSerializerViewSet, UUIDLookupFieldMixin


class UserViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = get_user_model().objects.all()
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }
    filterset_fields = ('full_name', 'email', 'is_staff', 'is_active',)


class GroupViewSet(MultiSerializerViewSet):
    queryset = Group.objects.all()
    serializers = {
        'default': GroupSerializer,
    }


class PermissionViewSet(MultiSerializerViewSet):
    queryset = Permission.objects.all()
    serializers = {
        'default': PermissionSerializer,
    }


class StudentProfileViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = StudentProfile.objects.all()
    serializers = {
        'default': StudentProfileSerializer,
    }


class InstructorProfileViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = InstructorProfile.objects.all()
    serializers = {
        'default': InstructorProfileSerializer,
    }
