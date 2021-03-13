from django.urls import path, include, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from accounts.models import CustomUser, UserRoles


class CustomUserTests(APITestCase, URLPatternsTestCase):
    """Test module for CustomUser."""

    urlpatterns = [
        path('api/accounts/', include('accounts.urls')),
    ]

    def setUp(self):
        """Create test users."""
        self.user = CustomUser.objects.create_user(
            full_name='Jane Doe',
            email='test1@test.com',
            password='test',
            role=UserRoles.STUDENT,
        )

        self.admin = CustomUser.objects.create_superuser(
            full_name='John Doe',
            email='admin@test.com',
            password='admin',
        )

        self.login_url = reverse('rest_login')

    def test_login(self):
        """Test if a user can login and get a JWT response token."""
        data = {
            'email': 'test1@test.com',
            'password': 'test',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_login(self):
        """Test if an admin can login and get a JWT response token."""
        data = {
            'email': 'admin@test.com',
            'password': 'admin',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_password(self):
        """Test if user can login with invalid password."""
        data = {
            'email': 'test1@test.com',
            'password': 'invalid',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        """Test if user can login with invalid data."""
        data = {
            'email': 'invalid@test.com',
            'password': 'invalid',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
