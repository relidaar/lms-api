from django.db.models import Q
from django_filters import rest_framework as filters

from accounts.models import InstructorProfile, StudentProfile
from education.models import (
    Assignment,
    Course,
    Event,
    EventType,
    Grade,
    NonPeriodicEventDetails,
    PeriodicEventDetails,
    Solution,
    StudentGroup,
    Timetable,
)


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

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(student_groups__in=user.studentprofile.student_groups)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(instructors=user.instructorprofile)
        return parent


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

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(course__student_groups__in=user.studentprofile.student_groups)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(course__instructors=user.instructorprofile)
        return parent


class TimetableItemFilter(filters.FilterSet):
    timetable = filters.ModelChoiceFilter(
        label='Timetable',
        field_name='uuid',
        to_field_name='uuid',
        queryset=Timetable.objects.all(),
    )

    instructor = filters.ModelChoiceFilter(
        label='Instructor',
        field_name='uuid',
        to_field_name='uuid',
        queryset=InstructorProfile.objects.all(),
    )

    students = filters.ModelMultipleChoiceFilter(
        label='Students',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentProfile.objects.all(),
    )

    class Meta:
        abstract = True
        fields = (
            'title', 'timetable', 'instructor', 'students', 'start_time',
            'end_time',
        )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(students=user.studentprofile)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(instructors=user.instructorprofile)
        return parent


class PeriodicTimetableItemFilter(TimetableItemFilter):
    class Meta:
        abstract = True
        fields = TimetableItemFilter.Meta.fields + ('weekday', 'repeat_type',)


class NonPeriodicTimetableItemFilter(TimetableItemFilter):
    class Meta:
        abstract = True
        fields = TimetableItemFilter.Meta.fields + ('date',)


class AssignmentFilter(NonPeriodicTimetableItemFilter):
    class Meta:
        model = Assignment
        fields = NonPeriodicTimetableItemFilter.Meta.fields + ()


class SolutionFilter(filters.FilterSet):
    assignment = filters.ModelChoiceFilter(
        label='Assignment',
        field_name='uuid',
        to_field_name='uuid',
        queryset=Assignment.objects.all(),
    )

    student = filters.ModelChoiceFilter(
        label='Student',
        field_name='uuid',
        to_field_name='uuid',
        queryset=StudentProfile.objects.all(),
    )

    class Meta:
        model = Solution
        fields = ('assignment', 'student', 'created_at',)

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(student=user.studentprofile)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(assignment__instructor=user.instructorprofile)
        return parent


class GradeFilter(filters.FilterSet):
    solution = filters.ModelChoiceFilter(
        label='Solution',
        field_name='uuid',
        to_field_name='uuid',
        queryset=Solution.objects.all(),
    )

    instructor = filters.ModelChoiceFilter(
        label='Instructor',
        field_name='uuid',
        to_field_name='uuid',
        queryset=InstructorProfile.objects.all(),
    )

    class Meta:
        model = Grade
        fields = ('value', 'solution', 'instructor', 'created_at',)

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(solution__student=user.studentprofile)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(instructor=user.instructorprofile)
        return parent


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

        if hasattr(user, 'user.studentprofile'):
            return parent.filter(timetable__course__student_groups__in=user.studentprofile.student_groups)
        if hasattr(user, 'user.instructorprofile'):
            return parent.filter(timetable__course__instructors=user.instructorprofile)

        return parent

    class Meta:
        model = Event
        fields = (
            'title', 'event_type', 'event_type__title', 'timetable',
            'timetable__code',
        )
