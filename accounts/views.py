from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserRoles
from accounts.serializers import UserSerializer


class IsAdmin(IsAuthenticated):
    allowed_user_roles = (UserRoles.ADMIN,)

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role in self.allowed_user_roles

    def has_object_permission(self, request, view, obj):
        return request.user.role in self.allowed_user_roles


class IsAccountOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.uuid == request.user.uuid


class UserListAPIView(ListAPIView):
    permission_classes = [IsAdmin]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailsAPIView(RetrieveAPIView):
    permission_classes = [IsAccountOwner | IsAdmin]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = get_object_or_404(self.queryset, uuid=self.kwargs.get('uuid'))
        self.check_object_permissions(self.request, obj)
        return obj


class UserCreateAPIView(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    pass