from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import StudentGroup, StudentProfile, InstructorProfile

User = get_user_model()


class TestData:
    def __init__(self):
        self.login_url = reverse('rest_login')
        self.superuser_login_data = {
            'email': 'superuser@test.com',
            'password': 'test',
        }

        self.superuser = User.objects.create_superuser(
            full_name='John Doe',
            email=self.superuser_login_data['email'],
            password=self.superuser_login_data['password'],
        )

        self.user1 = User.objects.create_user(
            full_name='Jack Doe',
            email='jack.doe@test.com',
            password='test',
        )

        self.user2 = User.objects.create_user(
            full_name='Jill Doe',
            email='jill.doe@test.com',
            password='test',
        )

        self.student = StudentProfile.objects.create(user=self.user1)
        self.instructor = InstructorProfile.objects.create(user=self.user2)

        self.student_group = StudentGroup.objects.create(code='TG4316')
        self.student_group.students.add(self.student)

    def login_as_superuser(self, client):
        client.post(self.login_url, self.superuser_login_data)


class UserCrudTests(APITestCase):
    """Test module for CRUD actions on users."""

    def setUp(self) -> None:
        """Create test users."""
        self.test_data = TestData()

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.user_list_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'uuid': self.test_data.superuser.uuid})

    def test_get_all_users(self):
        """Test if user can retrieve users list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_not_authenticated(self):
        """Test if not authenticated user can retrieve users list."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_user(self):
        """Test if user can retrieve valid details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_invalid_single_user(self):
        """Test if user can retrieve invalid details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(reverse('user-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_user(self):
        """Test if admin can create valid user."""
        data = {
            'full_name': 'Jane Doe',
            'email': 'jane.doe@test.com',
            'password': 'test',
        }
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        """Test if admin can create invalid user."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.user_list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_not_authenticated(self):
        """Test if not authenticated user can create new user."""
        response = self.client.post(self.user_list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_account_details(self):
        """Test if user can valid update account details."""
        data = {
            'full_name': self.test_data.superuser.full_name,
            'email': 'john.doe@test.com',
        }
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.user_detail_url, data=data)
        patch_response = self.client.patch(self.user_detail_url, data={'email': 'admin@test.com'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_account_details(self):
        """Test if user can invalid update account details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.user_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_account_details_not_authenticated(self):
        """Test if not authenticated user can update account details."""
        response = self.client.put(self.user_detail_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        """Test if user can delete another user."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(reverse('user-detail', kwargs={'uuid': self.test_data.user1.uuid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_not_authenticated(self):
        """Test if not authenticated user can delete another user."""
        response = self.client.delete(
            reverse('user-detail', kwargs={'uuid': self.test_data.user1.uuid}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StudentGroupCrudTests(APITestCase):
    """Test module for CRUD actions on student groups."""

    def setUp(self) -> None:
        self.test_data = TestData()
        student2 = StudentProfile.objects.create(user=self.test_data.user2)

        self.test_object = {
            'code': 'group2',
            'students': [
                reverse('student-detail', kwargs={'uuid': student2.uuid}),
            ]
        }

        self.list_endpoint = 'student-group-list'
        self.detail_endpoint = 'student-group-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={'uuid': self.test_data.student_group.uuid})

    def test_get_all_student_groups(self):
        """Test if superuser can retrieve student groups list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_student_groups_not_authenticated(self):
        """Test if not authenticated user can retrieve student groups list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_student_group(self):
        """Test if superuser can retrieve valid student group details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_student_group_not_authenticated(self):
        """Test if not authenticated user can retrieve student group details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_student_group(self):
        """Test if superuser can retrieve invalid student group details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_student_group(self):
        """Test if superuser can create valid student group."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_student_group(self):
        """Test if superuser can create invalid student group."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_group_not_authenticated(self):
        """Test if not authenticated user can create new student group."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_student_group_details(self):
        """Test if superuser can valid update student group details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'code': 'group41'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_student_group_details(self):
        """Test if superuser can invalid update student group details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_group_details_not_authenticated(self):
        """Test if not authenticated user can update student group details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_student_group(self):
        """Test if superuser can delete student group."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_student_group_not_authenticated(self):
        """Test if not authenticated user can delete student group."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
