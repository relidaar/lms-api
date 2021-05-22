from datetime import datetime
from uuid import uuid4

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import StudentProfile, InstructorProfile, StudentGroup
from education.models import (
    Course,
    Timetable,
    EventType,
    Event,
    PeriodicEventDetails,
    NonPeriodicEventDetails,
    PeriodicTimetableItem,
    Assignment,
    Solution,
    Grade,
)

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

        self.event = Event.objects.create(
            title='Test Event',
            event_type=self.event_type,
            timetable=self.timetable,
        )
        self.periodic_event_details = PeriodicEventDetails.objects.create(
            event=self.event,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            weekday=PeriodicTimetableItem.WeekDay.Monday,
            repeat_type=PeriodicTimetableItem.RepeatType.Weekly,
            instructor=self.instructor,
        )
        self.periodic_event_details.students.add(self.student)

        self.nonperiodic_event_details = NonPeriodicEventDetails.objects.create(
            event=self.event,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            date=datetime.now().date(),
            instructor=self.instructor,
        )
        self.nonperiodic_event_details.students.add(self.student)

        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            timetable=self.timetable,
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
            instructor=self.instructor,
            date=datetime.now().date(),
        )
        self.assignment.students.add(self.student)

        self.solution = Solution.objects.create(
            assignment=self.assignment,
            student=self.student,
        )

        self.grade = Grade.objects.create(
            value=90,
            solution=self.solution,
            instructor=self.instructor,
        )

    def login_as_superuser(self, client):
        client.post(self.login_url, self.superuser_login_data)


class CourseCrudTests(APITestCase):
    """Test module for CRUD actions on courses."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'code': 'course2',
            'title': 'Course 2',
            'instructors': [reverse('instructor-detail', kwargs={
                'uuid': self.test_data.instructor.uuid,
            })],
            'student_groups': [reverse('student-group-detail', kwargs={
                'uuid': self.test_data.student_group.uuid,
            })],
            'contents': [],
        }

        self.list_endpoint = 'course-list'
        self.detail_endpoint = 'course-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={'uuid': self.test_data.course.uuid})

    def test_get_all_courses(self):
        """Test if superuser can retrieve courses list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_courses_not_authenticated(self):
        """Test if not authenticated user can retrieve courses list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_course(self):
        """Test if superuser can retrieve valid course details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_course_not_authenticated(self):
        """Test if not authenticated user can retrieve course details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_course(self):
        """Test if superuser can delete course."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_not_authenticated(self):
        """Test if not authenticated user can delete course."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TimetableCrudTests(APITestCase):
    """Test module for CRUD actions on timetables."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'code': 'tt2',
            'title': 'Timetable 2',
            'course': reverse('course-detail', kwargs={
                'uuid': self.test_data.course.uuid,
            }),
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
        }

        self.list_endpoint = 'timetable-list'
        self.detail_endpoint = 'timetable-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={'uuid': self.test_data.timetable.uuid})

    def test_get_all_timetables(self):
        """Test if superuser can retrieve timetables list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_timetables_not_authenticated(self):
        """Test if not authenticated user can retrieve timetables list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_timetable(self):
        """Test if superuser can retrieve valid timetable details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_timetable_not_authenticated(self):
        """Test if not authenticated user can retrieve timetable details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_timetable(self):
        """Test if superuser can delete timetable."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_timetable_not_authenticated(self):
        """Test if not authenticated user can delete timetable."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_event_types_not_authenticated(self):
        """Test if not authenticated user can retrieve event types list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_event_type(self):
        """Test if superuser can retrieve valid event type details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_event_type_not_authenticated(self):
        """Test if not authenticated user can retrieve event type details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event_type(self):
        """Test if superuser can delete event type."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_type_not_authenticated(self):
        """Test if not authenticated user can delete event type."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class EventCrudTests(APITestCase):
    """Test module for CRUD actions on events."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'title': 'Test Event 2',
            'timetable': reverse('timetable-detail', kwargs={
                'uuid': self.test_data.timetable.uuid,
            }),
            'event_type': reverse('event-type-detail', kwargs={
                'uuid': self.test_data.event_type.uuid,
            }),
            'periodic_event_details': [],
            'non_periodic_event_details': [],
        }

        self.list_endpoint = 'event-list'
        self.detail_endpoint = 'event-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
            'uuid': self.test_data.event.uuid})

    def test_get_all_events(self):
        """Test if superuser can retrieve event list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_event_not_authenticated(self):
        """Test if not authenticated user can retrieve event list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_event(self):
        """Test if superuser can retrieve valid event details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_event_not_authenticated(self):
        """Test if not authenticated user can retrieve event details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_event(self):
        """Test if superuser can retrieve invalid event details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_event(self):
        """Test if superuser can create valid event."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event(self):
        """Test if superuser can create invalid event."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_event_not_authenticated(self):
        """Test if not authenticated user can create new event."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_event_details(self):
        """Test if superuser can valid update event details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'title': 'Assignment 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_event_details(self):
        """Test if superuser can invalid update event details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_event_details_not_authenticated(self):
        """Test if not authenticated user can update event details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event(self):
        """Test if superuser can delete event."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_not_authenticated(self):
        """Test if not authenticated user can delete event."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AssignmentCrudTests(APITestCase):
    """Test module for CRUD actions on assignments."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'title': 'Test Assignment 2',
            'timetable': reverse('timetable-detail', kwargs={
                'uuid': self.test_data.timetable.uuid,
            }),
            'start_time': datetime.now().time(),
            'end_time': datetime.now().time(),
            'instructor': reverse('instructor-detail', kwargs={
                'uuid': self.test_data.instructor.uuid,
            }),
            'date': '2021-05-22T07:48:44.968Z',
            'students': [
                reverse('student-detail', kwargs={
                    'uuid': self.test_data.student.uuid,
                })
            ]
        }

        self.list_endpoint = 'assignment-list'
        self.detail_endpoint = 'assignment-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
            'uuid': self.test_data.assignment.uuid})

    def test_get_all_assignments(self):
        """Test if superuser can retrieve assignment list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_assignments_not_authenticated(self):
        """Test if not authenticated user can retrieve assignment list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_assignment(self):
        """Test if superuser can retrieve valid assignment details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_assignment_not_authenticated(self):
        """Test if not authenticated user can retrieve assignment details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_assignment(self):
        """Test if superuser can retrieve invalid assignment details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_assignment(self):
        """Test if superuser can create valid assignment."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_assignment(self):
        """Test if superuser can create invalid assignment."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_assignment_not_authenticated(self):
        """Test if not authenticated user can create new assignment."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_assignment_details(self):
        """Test if superuser can valid update assignment details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'title': 'Assignment 3'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_assignment_details(self):
        """Test if superuser can invalid update assignment details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_assignment_details_not_authenticated(self):
        """Test if not authenticated user can update assignment details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_assignment(self):
        """Test if superuser can delete assignment."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_assignment_not_authenticated(self):
        """Test if not authenticated user can delete assignment."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SolutionCrudTests(APITestCase):
    """Test module for CRUD actions on solutions."""

    def setUp(self) -> None:
        self.test_data = TestData()

        self.test_object = {
            'assignment': reverse('assignment-detail', kwargs={
                'uuid': self.test_data.assignment.uuid,
            }),
            'student': reverse('student-detail', kwargs={
                'uuid': self.test_data.student.uuid,
            }),
        }

        self.list_endpoint = 'solution-list'
        self.detail_endpoint = 'solution-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
            'uuid': self.test_data.solution.uuid})

    def test_get_all_solutions(self):
        """Test if superuser can retrieve solution list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_solutions_not_authenticated(self):
        """Test if not authenticated user can retrieve solution list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_solution(self):
        """Test if superuser can retrieve valid solution details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_solution_not_authenticated(self):
        """Test if not authenticated user can retrieve solution details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_solution(self):
        """Test if superuser can retrieve invalid solution details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_solution(self):
        """Test if superuser can create valid solution."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_solution(self):
        """Test if superuser can create invalid solution."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_solution_not_authenticated(self):
        """Test if not authenticated user can create new solution."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_solution_details(self):
        """Test if superuser can valid update solution details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'comment': 'Comment'})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_solution_details(self):
        """Test if superuser can invalid update solution details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_solution_details_not_authenticated(self):
        """Test if not authenticated user can update solution details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_solution(self):
        """Test if superuser can delete solution."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_solution_not_authenticated(self):
        """Test if not authenticated user can delete solution."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GradeCrudTests(APITestCase):
    """Test module for CRUD actions on grades."""

    def setUp(self) -> None:
        self.test_data = TestData()

        solution = Solution.objects.create(
            assignment=self.test_data.assignment,
            student=self.test_data.student,
        )
        self.test_object = {
            'value': 80,
            'solution': reverse('solution-detail', kwargs={
                'uuid': solution.uuid,
            }),
            'instructor': reverse('instructor-detail', kwargs={
                'uuid': self.test_data.instructor.uuid,
            }),
        }

        self.list_endpoint = 'grade-list'
        self.detail_endpoint = 'grade-detail'
        self.list_url = reverse(self.list_endpoint)
        self.detail_url = reverse(self.detail_endpoint, kwargs={
            'uuid': self.test_data.grade.uuid})

    def test_get_all_grades(self):
        """Test if superuser can retrieve grade list."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_grades_not_authenticated(self):
        """Test if not authenticated user can retrieve grade list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_valid_single_grade(self):
        """Test if superuser can retrieve valid grade details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_grade_not_authenticated(self):
        """Test if not authenticated user can retrieve grade details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_invalid_single_grade(self):
        """Test if superuser can retrieve invalid grade details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.get(
            reverse(self.detail_endpoint, kwargs={'uuid': uuid4()}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_grade(self):
        """Test if superuser can create valid grade."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url, self.test_object)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_grade(self):
        """Test if superuser can create invalid grade."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_grade_not_authenticated(self):
        """Test if not authenticated user can create new grade."""
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_update_grade_details(self):
        """Test if superuser can valid update grade details."""
        self.test_data.login_as_superuser(self.client)
        put_response = self.client.put(self.detail_url, self.test_object)
        patch_response = self.client.patch(self.detail_url, {'value': 50})
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_invalid_update_grade_details(self):
        """Test if superuser can invalid update grade details."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_grade_details_not_authenticated(self):
        """Test if not authenticated user can update grade details."""
        response = self.client.put(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_grade(self):
        """Test if superuser can delete grade."""
        self.test_data.login_as_superuser(self.client)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_grade_not_authenticated(self):
        """Test if not authenticated user can delete grade."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
