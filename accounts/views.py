from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ModelViewSet
from django_auto_prefetching import AutoPrefetchViewSetMixin

from accounts.models import StudentProfile, InstructorProfile
from accounts.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PermissionSerializer, \
    StudentProfileSerializer, InstructorProfileSerializer
from config.views import MultiSerializerMixin, UUIDLookupFieldMixin


class UserViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = get_user_model().objects.all()
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }
    filterset_fields = ('full_name', 'email', 'is_staff', 'is_active',)
    search_fields = ('full_name', 'email',)


class GroupViewSet(ModelViewSet, MultiSerializerMixin, AutoPrefetchViewSetMixin):
    queryset = Group.objects.all()
    serializers = {
        'default': GroupSerializer,
    }


class PermissionViewSet(ModelViewSet, MultiSerializerMixin, AutoPrefetchViewSetMixin):
    queryset = Permission.objects.all()
    serializers = {
        'default': PermissionSerializer,
    }


class StudentProfileViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = StudentProfile.objects.all()
    serializers = {
        'default': StudentProfileSerializer,
    }
    filterset_fields = ('user', 'user__full_name', 'user__email',)


class InstructorProfileViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = InstructorProfile.objects.all()
    serializers = {
        'default': InstructorProfileSerializer,
    }
    filterset_fields = ('user', 'user__full_name', 'user__email',)
