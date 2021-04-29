from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ModelViewSet

from accounts.models import StudentProfile, InstructorProfile
from accounts.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PermissionSerializer, \
    StudentProfileSerializer, InstructorProfileSerializer
from config.views import MultiSerializerMixin, UUIDLookupFieldMixin


class UserViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = get_user_model().objects.all()
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }
    filterset_fields = ('full_name', 'email', 'is_staff', 'is_active',)
    search_fields = ('full_name', 'email',)


class GroupViewSet(ModelViewSet, MultiSerializerMixin):
    queryset = Group.objects.all()
    serializers = {
        'default': GroupSerializer,
    }


class PermissionViewSet(ModelViewSet, MultiSerializerMixin):
    queryset = Permission.objects.all()
    serializers = {
        'default': PermissionSerializer,
    }


class StudentProfileViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = StudentProfile.objects.all()
    serializers = {
        'default': StudentProfileSerializer,
    }
    filterset_fields = ('user', 'user__full_name', 'user__email',)


class InstructorProfileViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = InstructorProfile.objects.all()
    serializers = {
        'default': InstructorProfileSerializer,
    }
    filterset_fields = ('user', 'user__full_name', 'user__email',)
