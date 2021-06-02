from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class ApiRootView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({
            'api-v1': request.build_absolute_uri('/api/v1/'),

            'login': reverse('rest_login', request=request),
            'logout': reverse('rest_logout', request=request),
            'change-password': reverse('rest_password_change', request=request),
            'reset-password': reverse('rest_password_reset', request=request),
            'reset-password-confirm': reverse('rest_password_reset_confirm', request=request),

            'get-token': reverse('token_obtain_pair', request=request),
            'refresh-token': reverse('token_refresh', request=request),
            'verify-token': reverse('token_verify', request=request),

            'api-schema': reverse('schema', request=request),
            'swagger': reverse('swagger', request=request),
            'redoc': reverse('redoc', request=request),
        })
