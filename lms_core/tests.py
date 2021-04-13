from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import StudentProfile, InstructorProfile
from lms_core.models import StudentGroup, Course
from lms_core.serializers import StudentGroupSerializer, CourseSerializer

User = get_user_model()


class StudentGroupCrudTests(APITestCase):
    """Test module for CRUD actions on student groups."""

    def setUp(self) -> None:
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

        self.student1 = StudentProfile.objects.create(user=self.user1)
        self.student2 = StudentProfile.objects.create(user=self.user2)

        self.student_group1 = StudentGroup.objects.create(code='group1')
        self.student_group1.students.add(self.student1)

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('student-group-list')
        self.detail_url = reverse('student-group-detail', kwargs={'uuid': self.student_group1.uuid})

    def test_get_all_student_groups(self):
        """Test if superuser can retrieve student groups list."""
        self.client.post(self.login_url, self.superuser_login_data)

        self.student_group2 = StudentGroup.objects.create(code='group2')
        self.student_group2.students.add(self.student2)

        response = self.client.get(self.list_url)
        student_groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(student_groups, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_student_groups_not_authenticated(self):
        """Test if not authenticated user can retrieve student groups list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_student_group(self):
        """Test if superuser can retrieve valid student group details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        group = StudentGroup.objects.get(uuid=self.student_group1.uuid)
        serializer = StudentGroupSerializer(group)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_student_group_not_authenticated(self):
        """Test if not authenticated user can retrieve student group details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_student_group(self):
        """Test if superuser can retrieve invalid student group details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('student-group-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_student_group(self):
        """Test if superuser can create valid student group."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'code': 'group2',
            'students': [self.student2.pk]
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_student_group(self):
        """Test if superuser can create invalid student group."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_group_not_authenticated(self):
        """Test if not authenticated user can create new student group."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_student_group_details(self):
        """Test if superuser can valid update student group details."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'code': 'group51',
            'students': [self.student1.pk]
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'code': 'group41'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_student_group_details(self):
        """Test if superuser can invalid update student group details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_student_group_details_not_authenticated(self):
        """Test if not authenticated user can update student group details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_group(self):
        """Test if superuser can delete student group."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_student_group_not_authenticated(self):
        """Test if not authenticated user can delete student group."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseCrudTests(APITestCase):
    """Test module for CRUD actions on courses."""

    def setUp(self) -> None:
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

        self.student_group = StudentGroup.objects.create(code='group1')
        self.student_group.students.add(self.student)

        self.course = Course.objects.create(code='course1', title='Course 1')
        self.course.instructors.add(self.instructor)
        self.course.student_groups.add(self.student_group)

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('course-list')
        self.detail_url = reverse('course-detail', kwargs={'uuid': self.course.uuid})

    def test_get_all_courses(self):
        """Test if superuser can retrieve courses list."""
        self.client.post(self.login_url, self.superuser_login_data)

        self.course2 = Course.objects.create(code='course2', title='Course 2')
        self.course2.instructors.add(self.instructor)
        self.course2.student_groups.add(self.student_group)

        response = self.client.get(self.list_url)
        data = Course.objects.all()
        serializer = CourseSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_courses_not_authenticated(self):
        """Test if not authenticated user can retrieve courses list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_course(self):
        """Test if superuser can retrieve valid course details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        data = Course.objects.get(uuid=self.course.uuid)
        serializer = CourseSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_course_not_authenticated(self):
        """Test if not authenticated user can retrieve course details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_course(self):
        """Test if superuser can retrieve invalid course details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('course-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_course(self):
        """Test if superuser can create valid course."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'code': 'course2',
            'title': 'Course 2',
            'instructors': [self.instructor.pk],
            'student_groups': [self.student_group.pk],
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_course(self):
        """Test if superuser can create invalid course."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_course_not_authenticated(self):
        """Test if not authenticated user can create new course."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_course_details(self):
        """Test if superuser can valid update course details."""
        self.client.post(self.login_url, self.superuser_login_data)
        data = {
            'code': 'course2',
            'title': 'Course 2',
            'instructors': [self.instructor.pk],
            'student_groups': [self.student_group.pk],
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'code': 'course5'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_course_details(self):
        """Test if superuser can invalid update course details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_course_details_not_authenticated(self):
        """Test if not authenticated user can update course details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course(self):
        """Test if superuser can delete course."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_not_authenticated(self):
        """Test if not authenticated user can delete course."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
