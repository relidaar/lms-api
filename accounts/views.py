from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PermissionSerializer


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class UserViewSet(MultiSerializerViewSet):
    queryset = get_user_model().objects.all()
    lookup_field = 'uuid'
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
