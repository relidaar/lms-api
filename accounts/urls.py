from django.urls import include, path
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet, GroupViewSet, PermissionViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')
router.register('permissions', PermissionViewSet, basename='permission')

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
] + router.urls
