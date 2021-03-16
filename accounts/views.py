from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView

from accounts.serializers import UserSerializer, UserUpdateSerializer


class UserListAPIView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailsAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'


class UserCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView, RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'uuid'
