from django.urls import include, path

from accounts.views import UserListAPIView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', UserListAPIView.as_view(), name='users-list'),
]
