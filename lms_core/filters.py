from django_filters import rest_framework as filters
from django.db.models import Q

from accounts.models import InstructorProfile, StudentProfile
from lms_core.models import Course, Event, EventType, NonPeriodicEventDetails, PeriodicEventDetails, StudentGroup, Timetable


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

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        students = StudentProfile.objects.filter(user=user)
        instructors = InstructorProfile.objects.filter(user=user)

        if students:
            student = students.first()
            student_group = student.groups.first()
            return parent.filter(student_groups=student_group)
        if instructors:
            instructor = instructors.first()
            return parent.filter(instructors=instructor)
        return parent


class StudentGroupFilter(filters.FilterSet):
    students = filters.ModelMultipleChoiceFilter(
        label='Students',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentProfile.objects.all(),
    )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        students = StudentProfile.objects.filter(user=user)

        if not students:
            return parent

        student = students.first()
        return parent.filter(students=student)

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

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        students = StudentProfile.objects.filter(user=user)
        instructors = InstructorProfile.objects.filter(user=user)

        if students:
            student = students.first()
            periodic_events = PeriodicEventDetails.objects.filter(
                students=student
            )
            non_periodic_events = NonPeriodicEventDetails.objects.filter(
                students=student
            )
            return parent.filter(
                Q(periodic_event_details__in=periodic_events) |
                Q(non_periodic_event_details__in=non_periodic_events)
            )

        if instructors:
            instructor = instructors.first()
            periodic_events = PeriodicEventDetails.objects.filter(
                instructor=instructor
            )
            non_periodic_events = NonPeriodicEventDetails.objects.filter(
                instructor=instructor
            )

            return parent.filter(
                Q(periodic_event_details__in=periodic_events) |
                Q(non_periodic_event_details__in=non_periodic_events)
            )

        return parent

    class Meta:
        model = Event
        fields = (
            'title', 'event_type', 'event_type__title', 'timetable',
            'timetable__code',
        )
