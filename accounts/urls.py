from django.urls import include, path
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet, GroupViewSet, PermissionViewSet, StudentProfileViewSet, InstructorProfileViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')
router.register('permissions', PermissionViewSet, basename='permission')
router.register('students', StudentProfileViewSet, basename='student')
router.register('instructors', InstructorProfileViewSet, basename='instructor')

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
] + router.urls
