from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import path, include, reverse
from rest_framework import status

from accounts.models import UserRoles
from accounts.serializers import UserSerializer

User = get_user_model()

test_urlpatterns = [
    path('api/', include([
        path('users/', include('accounts.urls')),
    ])),
]

admin_login_data = {
    'email': 'admin@test.com',
    'password': 'admin',
}

user_login_data = {
    'email': 'test@test.com',
    'password': 'test',
}


class UserAuthTests(TestCase):
    """Test module for CustomUser."""
    urlpatterns = test_urlpatterns

    def setUp(self):
        """Create test users."""
        self.user = User.objects.create_user(
            full_name='Jane Doe',
            email=user_login_data['email'],
            password=user_login_data['password'],
            role=UserRoles.STUDENT,
        )

        self.admin = User.objects.create_superuser(
            full_name='John Doe',
            email=admin_login_data['email'],
            password=admin_login_data['password'],
        )

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')

    def test_login(self):
        """Test if a user can login and get a JWT response token."""
        response = self.client.post(self.login_url, user_login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_login(self):
        """Test if an admin can login and get a JWT response token."""
        response = self.client.post(self.login_url, admin_login_data)
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
        data = {
            'email': 'test1@test.com',
            'password': 'test',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_logout(self):
        """Test if an admin can logout."""
        data = {
            'email': 'admin@test.com',
            'password': 'admin',
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllUsersTests(TestCase):
    """Test module for user CRUD views."""
    urlpatterns = test_urlpatterns

    def setUp(self):
        self.user = User.objects.create_user(
            full_name='Jane Doe',
            email=user_login_data['email'],
            password=user_login_data['password'],
            role=UserRoles.STUDENT,
        )

        self.admin = User.objects.create_superuser(
            full_name='John Doe',
            email=admin_login_data['email'],
            password=admin_login_data['password'],
        )

        self.users = [self.user, self.admin]
        self.login_url = reverse('rest_login')
        self.get_users_list_url = reverse('users_list')

    def test_get_all_users(self):
        """Test if admin can retrieve users list."""
        self.client.post(self.login_url, admin_login_data)
        response = self.client.get(self.get_users_list_url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_not_authorized(self):
        """Test if not authorized user can retrieve users list."""
        self.client.post(self.login_url, user_login_data)
        response = self.client.get(self.get_users_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_not_authenticated(self):
        """Test if not authenticated user can retrieve users list."""
        response = self.client.get(self.get_users_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetSingleUserTests(TestCase):
    """Test module for user CRUD views."""
    urlpatterns = test_urlpatterns

    def setUp(self):
        self.user = User.objects.create_user(
            full_name='Jane Doe',
            email=user_login_data['email'],
            password=user_login_data['password'],
            role=UserRoles.STUDENT,
        )

        self.admin = User.objects.create_superuser(
            full_name='John Doe',
            email=admin_login_data['email'],
            password=admin_login_data['password'],
        )

        self.users = [self.user, self.admin]
        self.login_url = reverse('rest_login')

    def test_admin_get_valid_single_user(self):
        """Test if admin can retrieve valid single user."""
        self.client.post(self.login_url, admin_login_data)
        for user_to_test in self.users:
            response = self.client.get(reverse('get_user', kwargs={'uuid': user_to_test.uuid}))
            user = User.objects.get(uuid=user_to_test.uuid)
            serializer = UserSerializer(user)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_invalid_single_user(self):
        """Test if admin can retrieve invalid single user."""
        self.client.post(self.login_url, admin_login_data)
        response = self.client.get(reverse('get_user', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_get_account_details(self):
        """Test if user can retrieve account details."""
        self.client.post(self.login_url, user_login_data)
        response = self.client.get(reverse('get_user', kwargs={'uuid': self.user.uuid}))
        user = User.objects.get(uuid=self.user.uuid)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_another_account_details(self):
        """Test if user can retrieve another account details."""
        self.client.post(self.login_url, user_login_data)
        response = self.client.get(reverse('get_user', kwargs={'uuid': self.admin.uuid}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateUserTests(TestCase):
    """Test module for user CRUD views."""
    urlpatterns = test_urlpatterns

    def setUp(self):
        self.user = User.objects.create_user(
            full_name='Jane Doe',
            email=user_login_data['email'],
            password=user_login_data['password'],
            role=UserRoles.STUDENT,
        )

        self.admin = User.objects.create_superuser(
            full_name='John Doe',
            email=admin_login_data['email'],
            password=admin_login_data['password'],
        )

        self.user_to_create = {
            'full_name': 'Jack Doe',
            'email': 'test2@test.com',
            'password': 'test',
            'role': 'IN'
        }

        self.login_url = reverse('rest_login')
        self.create_user_url = reverse('create_user')

    def test_create_valid_user(self):
        """Test if admin can create valid user."""
        self.client.post(self.login_url, admin_login_data)
        response = self.client.post(self.create_user_url, data=self.user_to_create, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        """Test if admin can create invalid user."""
        data = {
            'full_name': '',
            'email': 'test2@test.com',
            'password': '',
            'role': 'IN'
        }
        self.client.post(self.login_url, admin_login_data)
        response = self.client.post(self.create_user_url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_not_authorized(self):
        """Test if not authorized user can create new user."""
        response = self.client.post(self.create_user_url, data=self.user_to_create, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_not_authenticated(self):
        """Test if not authenticated can create new user."""
        self.client.post(self.login_url, user_login_data)
        response = self.client.post(self.create_user_url, data=self.user_to_create, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
