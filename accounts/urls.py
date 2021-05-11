from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet, GroupViewSet, PermissionViewSet, StudentProfileViewSet, InstructorProfileViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('groups', GroupViewSet, basename='group')
router.register('permissions', PermissionViewSet, basename='permission')
router.register('students', StudentProfileViewSet, basename='student')
router.register('instructors', InstructorProfileViewSet, basename='instructor')

urlpatterns = [
] + router.urls
