from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from accounts.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PermissionSerializer
from config.views import MultiSerializerViewSet, UUIDViewSet


class UserViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = get_user_model().objects.all()
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }


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
