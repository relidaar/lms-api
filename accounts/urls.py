from django.urls import include, path

from accounts.views import UserListAPIView, UserDetailsAPIView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', UserListAPIView.as_view(), name='users_list'),
    path('<uuid:uuid>/', UserDetailsAPIView.as_view(), name='get_user'),
]
