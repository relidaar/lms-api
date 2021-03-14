from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserRoles
from accounts.serializers import UserSerializer


class IsAdmin(IsAuthenticated):
    allowed_user_roles = (UserRoles.ADMIN,)

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in self.allowed_user_roles


class UserListAPIView(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailsAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return get_user_model().objects.get(uuid=self.kwargs.get('uuid'))


class UserCreateAPIView(CreateAPIView):
    permission_classes = (IsAdmin,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
