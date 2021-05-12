from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework import viewsets
from django_auto_prefetching import AutoPrefetchViewSetMixin

from accounts.models import StudentProfile, InstructorProfile, StudentGroup
from api.accounts.serializers import (
    UserSerializer,
    UserUpdateSerializer,
    GroupSerializer,
    PermissionSerializer,
    StudentProfileSerializer,
    InstructorProfileSerializer,
    StudentGroupSerializer,
)
from api.common.views import MultiSerializerMixin, UUIDLookupFieldMixin
from api.accounts.filters import InstructorProfileFilter, StudentGroupFilter, StudentProfileFilter


class UserViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = get_user_model().objects.all()
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }
    filterset_fields = ('full_name', 'email', 'is_staff', 'is_active',)
    search_fields = ('full_name', 'email',)


class GroupViewSet(viewsets.ModelViewSet, MultiSerializerMixin, AutoPrefetchViewSetMixin):
    queryset = Group.objects.all()
    serializers = {
        'default': GroupSerializer,
    }


class PermissionViewSet(viewsets.ReadOnlyModelViewSet, MultiSerializerMixin, AutoPrefetchViewSetMixin):
    queryset = Permission.objects.all()
    serializers = {
        'default': PermissionSerializer,
    }


class StudentProfileViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = StudentProfile.objects.all()
    serializers = {
        'default': StudentProfileSerializer,
    }
    filterset_class = StudentProfileFilter


class InstructorProfileViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = InstructorProfile.objects.all()
    serializers = {
        'default': InstructorProfileSerializer,
    }
    filterset_class = InstructorProfileFilter


class StudentGroupViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }
    filterset_class = StudentGroupFilter
    search_fields = ('code',)
