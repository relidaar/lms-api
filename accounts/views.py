from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import UserSerializer, UserUpdateSerializer


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class UserViewSet(MultiSerializerViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    serializers = {
        'default': UserSerializer,
        'update': UserUpdateSerializer,
    }
