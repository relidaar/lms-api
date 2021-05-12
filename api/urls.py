from django import urls
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from api.views import ApiRootView
from api.urls_v1 import router as api_v1

urlpatterns = [
    path('', ApiRootView.as_view()),

    path('v1/', include(api_v1.urls)),

    path('auth/', include([
        path('', include('dj_rest_auth.urls'), name='dj_rest_auth'),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),

    path('docs/', include([
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'swagger/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger'
        ),
        path(
            'redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc'
        ),
    ])),
]
