from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import StudentProfile
from lms_core.models import StudentGroup
from lms_core.serializers import StudentGroupSerializer

User = get_user_model()


class StudentGroupCrudTests(APITestCase):
    """Test module for CRUD actions on student groups."""
    def setUp(self) -> None:
        self.admin_login_data = {
            'email': 'admin@test.com',
            'password': 'test',
        }

        self.admin = User.objects.create_superuser(
            full_name='John Doe',
            email=self.admin_login_data['email'],
            password=self.admin_login_data['password'],
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

        self.student1 = StudentProfile.objects.create(user=self.user1)
        self.student2 = StudentProfile.objects.create(user=self.user2)

        self.student_group1 = StudentGroup.objects.create(code='group1')
        self.student_group1.students.add(self.student1)

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.student_groups_list_url = reverse('student-group-list')
        self.student_group_detail_url = reverse('student-group-detail', kwargs={'uuid': self.student_group1.uuid})

    def test_get_all_student_groups(self):
        """Test if user can retrieve student groups list."""
        self.client.post(self.login_url, self.admin_login_data)

        self.student_group2 = StudentGroup.objects.create(code='group2')
        self.student_group2.students.add(self.student2)

        response = self.client.get(self.student_groups_list_url)
        student_groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(student_groups, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_student_groups_not_authenticated(self):
        """Test if not authenticated user can retrieve student groups list."""
        response = self.client.get(self.student_groups_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_student_group(self):
        """Test if admin can retrieve valid student group details."""
        self.client.post(self.login_url, self.admin_login_data)
        response = self.client.get(self.student_group_detail_url)
        group = StudentGroup.objects.get(uuid=self.student_group1.uuid)
        serializer = StudentGroupSerializer(group)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_invalid_single_student_group(self):
        """Test if admin can retrieve invalid student group details."""
        self.client.post(self.login_url, self.admin_login_data)
        response = self.client.get(reverse('student-group-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_student_group(self):
        """Test if admin can create valid student group."""
        self.client.post(self.login_url, self.admin_login_data)

        data = {
            'code': 'group2',
            'students': [self.student2.pk]
        }
        response = self.client.post(self.student_groups_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_student_group(self):
        """Test if admin can create invalid student group."""
        self.client.post(self.login_url, self.admin_login_data)
        response = self.client.post(self.student_groups_list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_group_not_authenticated(self):
        """Test if not authenticated user can create new student group."""
        response = self.client.post(self.student_groups_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_student_group_details(self):
        """Test if admin can valid update student group details."""
        self.client.post(self.login_url, self.admin_login_data)

        data = {
            'code': 'group51',
            'students': [self.student1.pk]
        }
        put_response = self.client.put(self.student_group_detail_url, data)
        patch_response = self.client.patch(self.student_group_detail_url, {'code': 'group41'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_student_group_details(self):
        """Test if admin can invalid update student group details."""
        self.client.post(self.login_url, self.admin_login_data)
        response = self.client.put(self.student_group_detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_group_details_not_authenticated(self):
        """Test if not authenticated user can update student group details."""
        response = self.client.put(self.student_group_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_group(self):
        """Test if admin can delete student group."""
        self.client.post(self.login_url, self.admin_login_data)
        response = self.client.delete(self.student_group_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_student_group_not_authenticated(self):
        """Test if not authenticated user can delete student group."""
        response = self.client.delete(self.student_group_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
