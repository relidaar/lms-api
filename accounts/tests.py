from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import path, include, reverse
from rest_framework import status

User = get_user_model()

test_urlpatterns = [
    path('api/', include([
        path('users/', include('accounts.urls')),
    ])),
]


class UserAuthTests(TestCase):
    """Test module for CustomUser."""
    urlpatterns = test_urlpatterns

    def setUp(self):
        """Create test users."""

        self.login_data = {
            'email': 'test@test.com',
            'password': 'test',
        }

        self.user = User.objects.create_user(
            full_name='Jane Doe',
            email=self.login_data['email'],
            password=self.login_data['password'],
        )

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')

    def test_login(self):
        """Test if a user can login and get a JWT response token."""
        response = self.client.post(self.login_url, self.login_data)
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

    def test_logout(self):
        """Test if a user can logout."""
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
