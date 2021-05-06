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

        self.course = Course.objects.create(code='TC4316', title='Test Course')
        self.course.instructors.add(self.instructor)
        self.course.student_groups.add(self.student_group)

        self.timetable = Timetable.objects.create(
            code='TT4316',
            title='Test Timetable',
            course=self.course,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        self.event_type = EventType.objects.create(title='Test Event Type')

        self.periodic_event = PeriodicEvent.objects.create(
            title='Test Periodic Event',
            event_type=self.event_type,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            timetable=self.timetable,
            weekday=PeriodicEvent.WeekDay.Monday,
            repeat_type=PeriodicEvent.RepeatType.Weekly,
            instructor=self.instructor,
        )
        self.periodic_event.students.add(self.student)

        self.nonperiodic_event = NonPeriodicEvent.objects.create(
            title='Test Non-Periodic Event',
            event_type=self.event_type,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            date=datetime.now().date(),
            timetable=self.timetable,
            instructor=self.instructor,
        )
        self.nonperiodic_event.students.add(self.student)

    def login_as_superuser(self, client):
        client.post(self.login_url, self.superuser_login_data)


class StudentGroupCrudTests(APITestCase):
    """Test module for CRUD actions on student groups."""

    def setUp(self) -> None:
        self.test_data = TestData()
        student2 = StudentProfile.objects.create(user=self.test_data.user2)

        self.test_object = {
            'code': 'group2',
            'students': [student2.pk]
        }

        self.list_endpoint = 'student-group-list'
        self.detail_endpoint = 'student-group-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
                                  'uuid': self.test_data.student_group.uuid})

    def test_get_all_student_groups(self):
        """Test if superuser can retrieve student groups list."""
        self.test_data.login_as_superuser(self.client)
        student_group2 = StudentGroup.objects.create(
            code=self.test_object['code'])
        for item in self.test_object['students']:
            student_group2.students.add(item)

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
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        group = StudentGroup.objects.get(
            uuid=self.test_data.student_group.uuid)
        serializer = StudentGroupSerializer(group)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_student_group_not_authenticated(self):
        """Test if not authenticated user can retrieve student group details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_student_group(self):
        """Test if superuser can retrieve invalid student group details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_student_group_details(self):
        """Test if superuser can valid update student group details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(
            self.detail_url, {'code': 'group41'})
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student_group(self):
        """Test if superuser can delete student group."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_student_group_not_authenticated(self):
        """Test if not authenticated user can delete student group."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseCrudTests(APITestCase):
    """Test module for CRUD actions on courses."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'code': 'course2',
            'title': 'Course 2',
            'instructors': [self.test_data.instructor.pk],
            'student_groups': [self.test_data.student_group.pk],
        }

        self.list_endpoint = 'course-list'
        self.detail_endpoint = 'course-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
                                  'uuid': self.test_data.course.uuid})

    def test_get_all_courses(self):
        """Test if superuser can retrieve courses list."""
        self.test_data.login_as_superuser(self.client)

        course2 = Course.objects.create(
            code=self.test_object['code'], title=self.test_object['title'])
        for item in self.test_object['instructors']:
            course2.instructors.add(item)
        for item in self.test_object['student_groups']:
            course2.student_groups.add(item)

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
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        data = Course.objects.get(uuid=self.test_data.course.uuid)
        serializer = CourseSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_course_not_authenticated(self):
        """Test if not authenticated user can retrieve course details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_course(self):
        """Test if superuser can retrieve invalid course details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_course(self):
        """Test if superuser can create valid course."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_course(self):
        """Test if superuser can create invalid course."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_course_not_authenticated(self):
        """Test if not authenticated user can create new course."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_course_details(self):
        """Test if superuser can valid update course details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(
            self.detail_url, {'code': 'course5'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_course_details(self):
        """Test if superuser can invalid update course details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_course_details_not_authenticated(self):
        """Test if not authenticated user can update course details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course(self):
        """Test if superuser can delete course."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_not_authenticated(self):
        """Test if not authenticated user can delete course."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TimetableCrudTests(APITestCase):
    """Test module for CRUD actions on timetables."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'code': 'tt2',
            'title': 'Timetable 2',
            'course': self.test_data.course.pk,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
        }

        self.list_endpoint = 'timetable-list'
        self.detail_endpoint = 'timetable-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
                                  'uuid': self.test_data.timetable.uuid})

    def test_get_all_timetables(self):
        """Test if superuser can retrieve timetables list."""
        self.test_data.login_as_superuser(self.client)

        Timetable.objects.create(
            code=self.test_object['code'],
            title=self.test_object['title'],
            course=Course.objects.get(pk=self.test_object['course']),
            start_date=self.test_object['start_date'],
            end_date=self.test_object['end_date'],
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
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        data = Timetable.objects.get(uuid=self.test_data.timetable.uuid)
        serializer = TimetableSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_timetable_not_authenticated(self):
        """Test if not authenticated user can retrieve timetable details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_timetable(self):
        """Test if superuser can retrieve invalid timetable details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_timetable(self):
        """Test if superuser can create valid timetable."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_timetable(self):
        """Test if superuser can create invalid timetable."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_timetable_not_authenticated(self):
        """Test if not authenticated user can create new timetable."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_timetable_details(self):
        """Test if superuser can valid update timetable details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'code': 'tt5'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_timetable_details(self):
        """Test if superuser can invalid update timetable details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_timetable_details_not_authenticated(self):
        """Test if not authenticated user can update timetable details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_timetable(self):
        """Test if superuser can delete timetable."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_timetable_not_authenticated(self):
        """Test if not authenticated user can delete timetable."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EventTypeCrudTests(APITestCase):
    """Test module for CRUD actions on event types."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'title': 'Event Type 2',
        }

        self.list_endpoint = 'event-type-list'
        self.detail_endpoint = 'event-type-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
                                  'uuid': self.test_data.event_type.uuid})

    def test_get_all_event_types(self):
        """Test if superuser can retrieve event types list."""
        self.test_data.login_as_superuser(self.client)

        EventType.objects.create(title=self.test_object['title'])

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
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        data = EventType.objects.get(uuid=self.test_data.event_type.uuid)
        serializer = EventTypeSerializer(data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_event_type_not_authenticated(self):
        """Test if not authenticated user can retrieve event type details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_single_event_type(self):
        """Test if superuser can retrieve invalid event type details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_event_type(self):
        """Test if superuser can create valid event type."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event_type(self):
        """Test if superuser can create invalid event type."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_type_not_authenticated(self):
        """Test if not authenticated user can create new event type."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_event_type_details(self):
        """Test if superuser can valid update event type details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(
            self.detail_url, {'title': 'Event 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_event_type_details(self):
        """Test if superuser can invalid update event type details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_event_type_details_not_authenticated(self):
        """Test if not authenticated user can update event type details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_event_type(self):
        """Test if superuser can delete event type."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_type_not_authenticated(self):
        """Test if not authenticated user can delete event type."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
