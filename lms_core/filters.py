from django_filters import rest_framework as filters

from accounts.models import InstructorProfile, StudentProfile
from lms_core.models import Course, Event, EventType, StudentGroup, Timetable


class CourseFilter(filters.FilterSet):
    instructors = filters.ModelMultipleChoiceFilter(
        label='Instructors',
        field_name='uuid',
        to_field_name='uuid',
        queryset=InstructorProfile.objects.all(),
    )

    student_groups = filters.ModelMultipleChoiceFilter(
        label='Student Groups',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentGroup.objects.all(),
    )

    class Meta:
        model = Course
        fields = ('code', 'title', 'instructors', 'student_groups',)


class StudentGroupFilter(filters.FilterSet):
    students = filters.ModelMultipleChoiceFilter(
        label='Students',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentProfile.objects.all(),
    )

    class Meta:
        model = StudentGroup
        fields = ('code', 'students',)


class TimetableFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(
        label='Course',
        field_name='uuid',
        to_field_name='uuid',
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Timetable
        fields = (
            'code', 'title', 'course', 'course__code', 'course__title',
            'start_date', 'end_date',
        )


class EventFilter(filters.FilterSet):
    event_type = filters.ModelChoiceFilter(
        label='Event Type',
        field_name='uuid',
        to_field_name='uuid',
        queryset=EventType.objects.all(),
    )

    timetable = filters.ModelChoiceFilter(
        label='Timetable',
        field_name='uuid',
        to_field_name='uuid',
        queryset=Timetable.objects.all(),
    )

    class Meta:
        model = Event
        fields = (
            'title', 'event_type', 'event_type__title', 'timetable',
            'timetable__code',
        )
