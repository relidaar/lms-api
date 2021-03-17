from django.urls import include, path
from rest_framework.routers import SimpleRouter

from accounts.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
] + router.urls
