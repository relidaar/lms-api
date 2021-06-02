from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthTests(APITestCase):
    """Test module for user authentication."""

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
