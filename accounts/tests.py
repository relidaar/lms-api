from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.serializers import UserSerializer

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


class UserCrudTests(APITestCase):
    """Test module for CRUD actions on users."""
    def setUp(self) -> None:
        """Create test users."""
        self.login_data = {
            'email': 'admin@test.com',
            'password': 'test',
        }

        self.user = User.objects.create_superuser(
            full_name='John Doe',
            email=self.login_data['email'],
            password=self.login_data['password'],
        )

        self.user2 = User.objects.create_user(
            full_name='Jack Doe',
            email='jack.doe@test.com',
            password='test',
        )

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.user_list_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'uuid': self.user.uuid})

    def test_get_all_users(self):
        """Test if user can retrieve users list."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.get(self.user_list_url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_not_authenticated(self):
        """Test if not authenticated user can retrieve users list."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_user(self):
        """Test if user can retrieve valid details."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.get(self.user_detail_url)
        user = User.objects.get(uuid=self.user.uuid)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_invalid_single_user(self):
        """Test if user can retrieve invalid details."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.get(reverse('user-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_user(self):
        """Test if admin can create valid user."""
        data = {
            'full_name': 'Jane Doe',
            'email': 'jane.doe@test.com',
            'password': 'test',
        }
        self.client.post(self.login_url, self.login_data)
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        """Test if admin can create invalid user."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.post(self.user_list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_not_authenticated(self):
        """Test if not authenticated user can create new user."""
        response = self.client.post(self.user_list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_account_details(self):
        """Test if user can valid update account details."""
        data = {
            'full_name': self.user.full_name,
            'email': 'john.doe@test.com',
        }
        self.client.post(self.login_url, self.login_data)
        put_response = self.client.put(self.user_detail_url, data=data)
        patch_response = self.client.patch(self.user_detail_url, data={'email': 'admin@test.com'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_account_details(self):
        """Test if user can invalid update account details."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.put(self.user_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_account_details_not_authenticated(self):
        """Test if not authenticated user can update account details."""
        response = self.client.put(self.user_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        """Test if user can delete another user."""
        self.client.post(self.login_url, self.login_data)
        response = self.client.delete(reverse('user-detail', kwargs={'uuid': self.user2.uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_not_authenticated(self):
        """Test if not authenticated user can delete another user."""
        response = self.client.delete(reverse('user-detail', kwargs={'uuid': self.user2.uuid}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
