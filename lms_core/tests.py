from datetime import datetime
from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import StudentProfile, InstructorProfile
from lms_core.models import StudentGroup, Course, Timetable, EventType, PeriodicEvent, NonPeriodicEvent
from lms_core.serializers import StudentGroupSerializer, CourseSerializer, TimetableSerializer, EventTypeSerializer, \
    PeriodicEventSerializer, NonPeriodicEventSerializer

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

        student_group2 = StudentGroup.objects.create(code='group2')
        student_group2.students.add(self.student2)

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

        course2 = Course.objects.create(code='course2', title='Course 2')
        course2.instructors.add(self.instructor)
        course2.student_groups.add(self.student_group)

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


class TimetableCrudTests(APITestCase):
    """Test module for CRUD actions on timetables."""

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

        self.timetable = Timetable.objects.create(
            code='tt1',
            title='Timetable 1',
            course=self.course,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('timetable-list')
        self.detail_url = reverse('timetable-detail', kwargs={'uuid': self.timetable.uuid})

    def test_get_all_timetables(self):
        """Test if superuser can retrieve timetables list."""
        self.client.post(self.login_url, self.superuser_login_data)

        Timetable.objects.create(
            code='tt2',
            title='Timetable 2',
            course=self.course,
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
        )

        response = self.client.get(self.list_url)
        data = Timetable.objects.all()
        serializer = TimetableSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_timetables_not_authenticated(self):
        """Test if not authenticated user can retrieve timetables list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_timetable(self):
        """Test if superuser can retrieve valid timetable details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        data = Timetable.objects.get(uuid=self.timetable.uuid)
        serializer = TimetableSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_timetable_not_authenticated(self):
        """Test if not authenticated user can retrieve timetable details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_timetable(self):
        """Test if superuser can retrieve invalid timetable details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('timetable-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_timetable(self):
        """Test if superuser can create valid timetable."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'code': 'tt2',
            'title': 'Timetable 2',
            'course': self.course.pk,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_timetable(self):
        """Test if superuser can create invalid timetable."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timetable_not_authenticated(self):
        """Test if not authenticated user can create new timetable."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_timetable_details(self):
        """Test if superuser can valid update timetable details."""
        self.client.post(self.login_url, self.superuser_login_data)
        data = {
            'code': 'tt2',
            'title': 'Timetable 2',
            'course': self.course.pk,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'code': 'tt5'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_timetable_details(self):
        """Test if superuser can invalid update timetable details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_timetable_details_not_authenticated(self):
        """Test if not authenticated user can update timetable details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_timetable(self):
        """Test if superuser can delete timetable."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_timetable_not_authenticated(self):
        """Test if not authenticated user can delete timetable."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventTypeCrudTests(APITestCase):
    """Test module for CRUD actions on event types."""

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

        self.event_type = EventType.objects.create(title='Event 1')

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('event-type-list')
        self.detail_url = reverse('event-type-detail', kwargs={'uuid': self.event_type.uuid})

    def test_get_all_event_types(self):
        """Test if superuser can retrieve event types list."""
        self.client.post(self.login_url, self.superuser_login_data)

        EventType.objects.create(title='Event 2')

        response = self.client.get(self.list_url)
        data = EventType.objects.all()
        serializer = EventTypeSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_event_types_not_authenticated(self):
        """Test if not authenticated user can retrieve event types list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_event_type(self):
        """Test if superuser can retrieve valid event type details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        data = EventType.objects.get(uuid=self.event_type.uuid)
        serializer = EventTypeSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_event_type_not_authenticated(self):
        """Test if not authenticated user can retrieve event type details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_event_type(self):
        """Test if superuser can retrieve invalid event type details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('event-type-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_event_type(self):
        """Test if superuser can create valid event type."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event_type(self):
        """Test if superuser can create invalid event type."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_type_not_authenticated(self):
        """Test if not authenticated user can create new event type."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_event_type_details(self):
        """Test if superuser can valid update event type details."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'title': 'Event 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_event_type_details(self):
        """Test if superuser can invalid update event type details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_event_type_details_not_authenticated(self):
        """Test if not authenticated user can update event type details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_type(self):
        """Test if superuser can delete event type."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_type_not_authenticated(self):
        """Test if not authenticated user can delete event type."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PeriodicEventCrudTests(APITestCase):
    """Test module for CRUD actions on periodic events."""

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

        self.timetable = Timetable.objects.create(
            code='tt1',
            title='Timetable 1',
            course=self.course,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        self.event_type = EventType.objects.create(title='Event Type 1')

        self.event = PeriodicEvent.objects.create(
            title='Event 1',
            event_type=self.event_type,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            timetable=self.timetable,
            weekday=PeriodicEvent.WeekDay.Monday,
            repeat_type=PeriodicEvent.RepeatType.Weekly,
            instructor=self.instructor,
        )
        self.event.students.add(self.student)

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('periodic-event-list')
        self.detail_url = reverse('periodic-event-detail', kwargs={'uuid': self.event.uuid})

    def test_get_all_periodic_events(self):
        """Test if superuser can retrieve periodic events list."""
        self.client.post(self.login_url, self.superuser_login_data)

        event = PeriodicEvent.objects.create(
            title='Event 2',
            event_type=self.event_type,
            start_time=datetime.now(),
            end_time=datetime.now(),
            timetable=self.timetable,
            weekday=PeriodicEvent.WeekDay.Monday,
            repeat_type=PeriodicEvent.RepeatType.Weekly,
            instructor=self.instructor,
        )
        event.students.add(self.student)

        response = self.client.get(self.list_url)
        data = PeriodicEvent.objects.all()
        serializer = PeriodicEventSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_periodic_events_not_authenticated(self):
        """Test if not authenticated user can retrieve periodic events list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_periodic_event(self):
        """Test if superuser can retrieve valid periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        data = PeriodicEvent.objects.get(uuid=self.event.uuid)
        serializer = PeriodicEventSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_periodic_event_not_authenticated(self):
        """Test if not authenticated user can retrieve periodic event details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_periodic_event(self):
        """Test if superuser can retrieve invalid periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('periodic-event-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_periodic_event(self):
        """Test if superuser can create valid periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
            'event_type': self.event_type.pk,
            'start_time': datetime.now().time(),
            'end_time': datetime.now().time(),
            'timetable': self.timetable.pk,
            'weekday': PeriodicEvent.WeekDay.Monday,
            'repeat_type': PeriodicEvent.RepeatType.Weekly,
            'instructor': self.instructor.pk,
            'students': [self.student.pk],
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_periodic_event(self):
        """Test if superuser can create invalid periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_periodic_event_not_authenticated(self):
        """Test if not authenticated user can create new periodic event."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_periodic_event_details(self):
        """Test if superuser can valid update periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
            'event_type': self.event_type.pk,
            'start_time': datetime.now().time(),
            'end_time': datetime.now().time(),
            'timetable': self.timetable.pk,
            'weekday': PeriodicEvent.WeekDay.Monday,
            'repeat_type': PeriodicEvent.RepeatType.Weekly,
            'instructor': self.instructor.pk,
            'students': [self.student.pk],
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'title': 'Event 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_periodic_event_details(self):
        """Test if superuser can invalid update periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_periodic_event_details_not_authenticated(self):
        """Test if not authenticated user can update periodic event details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_periodic_event(self):
        """Test if superuser can delete periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_periodic_event_not_authenticated(self):
        """Test if not authenticated user can delete periodic event."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class NonPeriodicEventCrudTests(APITestCase):
    """Test module for CRUD actions on non-periodic events."""

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

        self.timetable = Timetable.objects.create(
            code='tt1',
            title='Timetable 1',
            course=self.course,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        self.event_type = EventType.objects.create(title='Event Type 1')

        self.event = NonPeriodicEvent.objects.create(
            title='Event 1',
            event_type=self.event_type,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            date=datetime.now().date(),
            timetable=self.timetable,
            instructor=self.instructor,
        )
        self.event.students.add(self.student)

        self.login_url = reverse('rest_login')
        self.logout_url = reverse('rest_logout')
        self.list_url = reverse('nonperiodic-event-list')
        self.detail_url = reverse('nonperiodic-event-detail', kwargs={'uuid': self.event.uuid})

    def test_get_all_non_periodic_events(self):
        """Test if superuser can retrieve non-periodic events list."""
        self.client.post(self.login_url, self.superuser_login_data)

        event = NonPeriodicEvent.objects.create(
            title='Event 2',
            event_type=self.event_type,
            start_time=datetime.now(),
            end_time=datetime.now(),
            date=datetime.now().date(),
            timetable=self.timetable,
            instructor=self.instructor,
        )
        event.students.add(self.student)

        response = self.client.get(self.list_url)
        data = NonPeriodicEvent.objects.all()
        serializer = NonPeriodicEventSerializer(data, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_non_periodic_events_not_authenticated(self):
        """Test if not authenticated user can retrieve non-periodic events list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_valid_single_non_periodic_event(self):
        """Test if superuser can retrieve valid non-periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(self.detail_url)
        data = NonPeriodicEvent.objects.get(uuid=self.event.uuid)
        serializer = NonPeriodicEventSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_non_periodic_event_not_authenticated(self):
        """Test if not authenticated user can retrieve non-periodic event details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_non_periodic_event(self):
        """Test if superuser can retrieve invalid non-periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.get(reverse('nonperiodic-event-detail', kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_non_periodic_event(self):
        """Test if superuser can create valid non-periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
            'event_type': self.event_type.pk,
            'start_time': datetime.now().time(),
            'end_time': datetime.now().time(),
            'date': datetime.now().date(),
            'timetable': self.timetable.pk,
            'instructor': self.instructor.pk,
            'students': [self.student.pk],
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_non_periodic_event(self):
        """Test if superuser can create invalid non-periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_non_periodic_event_not_authenticated(self):
        """Test if not authenticated user can create new non-periodic event."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_non_periodic_event_details(self):
        """Test if superuser can valid update non-periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)

        data = {
            'title': 'Event 2',
            'event_type': self.event_type.pk,
            'start_time': datetime.now().time(),
            'end_time': datetime.now().time(),
            'date': datetime.now().date(),
            'timetable': self.timetable.pk,
            'instructor': self.instructor.pk,
            'students': [self.student.pk],
        }
        put_response = self.client.put(self.detail_url, data)
        patch_response = self.client.patch(self.detail_url, {'title': 'Event 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_non_periodic_event_details(self):
        """Test if superuser can invalid update non-periodic event details."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_non_periodic_event_details_not_authenticated(self):
        """Test if not authenticated user can update non-periodic event details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_periodic_event(self):
        """Test if superuser can delete non-periodic event."""
        self.client.post(self.login_url, self.superuser_login_data)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_periodic_event_not_authenticated(self):
        """Test if not authenticated user can delete non-periodic event."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
