from django.urls import include, path

from accounts.views import UserListAPIView, UserDetailsAPIView, UserCreateAPIView, UserUpdateAPIView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', UserListAPIView.as_view(), name='users_list'),
    path('add/', UserCreateAPIView.as_view(), name='create_user'),
    path('<uuid:uuid>/', UserDetailsAPIView.as_view(), name='get_user'),
    path('<uuid:uuid>/edit/', UserUpdateAPIView.as_view(), name='update_user'),
]
