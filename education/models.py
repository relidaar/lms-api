from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import InstructorProfile, StudentProfile, StudentGroup
from common.models import Content, UUIDFieldMixin


class Course(UUIDFieldMixin, models.Model):
    """Represent an academic course."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    syllabus = models.TextField(blank=True)
    instructors = models.ManyToManyField(
        InstructorProfile,
        related_name='instructed_courses',
    )
    student_groups = models.ManyToManyField(
        StudentGroup,
        related_name='joined_courses',
    )

    def __str__(self):
        return f'{self.code} - {self.title}'


class Timetable(UUIDFieldMixin, models.Model):
    """Represent an event timetable related to specific course."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='timetables',
    )
    start_date = models.DateField(verbose_name='Course start date')
    end_date = models.DateField(verbose_name='Course end date')

    def __str__(self):
        return f'{self.title} ({self.course.code} course)'


class TimetableItem(UUIDFieldMixin, models.Model):
    """Basic model for course events."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timetable = models.ForeignKey(
        Timetable,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
    )
    start_time = models.TimeField(verbose_name='Course event start time')
    end_time = models.TimeField(verbose_name='Course event end time')
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)ss',
    )
    students = models.ManyToManyField(
        StudentProfile,
        related_name='%(class)ss',
    )

    class Meta:
        abstract = True


class PeriodicTimetableItem(TimetableItem):
    """Basic model for periodic timetable items."""

    class WeekDay(models.TextChoices):
        Monday = 'MO', _('Monday')
        Tuesday = 'TU', _('Tuesday')
        Wednesday = 'WE', _('Wednesday')
        Thursday = 'TH', _('Thursday')
        Friday = 'FR', _('Friday')
        Saturday = 'SA', _('Saturday')
        Sunday = 'SU', _('Sunday')

    class RepeatType(models.TextChoices):
        Weekly = 'W', _('Weekly')
        Even = 'E', _('Even')
        Odd = 'O', _('Odd')

    weekday = models.CharField(
        choices=WeekDay.choices,
        default=WeekDay.Monday,
        max_length=2,
    )
    repeat_type = models.CharField(
        choices=RepeatType.choices,
        default=RepeatType.Weekly,
        max_length=1,
    )

    class Meta:
        abstract = True


class NonPeriodicTimetableItem(TimetableItem):
    """Basic model for non-periodic timetable items."""
    date = models.DateTimeField()

    class Meta:
        abstract = True


class Assignment(NonPeriodicTimetableItem):
    """Represent a course assignment related to event."""

    def __str__(self) -> str:
        return self.title


class Solution(UUIDFieldMixin, models.Model):
    """Represent student's solution to course assignment."""
    assignment = models.ForeignKey(
        Assignment,
        related_name='solutions',
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        StudentProfile,
        related_name='solutions',
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)


class Grade(UUIDFieldMixin, models.Model):
    """Represent a response to the student's solution."""
    value = models.PositiveSmallIntegerField(default=0)
    solution = models.OneToOneField(
        Solution,
        related_name='grade',
        on_delete=models.CASCADE,
    )
    instructor = models.ForeignKey(
        InstructorProfile,
        related_name='grades',
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)


class CourseContent(Content):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='contents',
    )


class AssignmentContent(Content):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='contents',
    )


class SolutionContent(Content):
    solution = models.ForeignKey(
        Solution,
        on_delete=models.CASCADE,
        related_name='contents',
    )


class EventType(UUIDFieldMixin, models.Model):
    """Represent types of timetable events."""
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Event(UUIDFieldMixin, models.Model):
    """Basic model for timetable events."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    timetable = models.ForeignKey(
        Timetable,
        on_delete=models.CASCADE,
        related_name='events'
    )

    def __str__(self):
        return f'{self.title} ({self.event_type.title})'


class EventDetails(UUIDFieldMixin, models.Model):
    """Basic details for course event."""
    start_time = models.TimeField(verbose_name='Event start time')
    end_time = models.TimeField(verbose_name='Event end time')
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.SET_NULL,
        null=True,
    )
    students = models.ManyToManyField(StudentProfile)

    class Meta:
        abstract = True


class PeriodicEventDetails(EventDetails):
    """Represent details for periodic course events."""
    weekday = models.CharField(
        choices=PeriodicTimetableItem.WeekDay.choices,
        default=PeriodicTimetableItem.WeekDay.Monday,
        max_length=2,
    )
    repeat_type = models.CharField(
        choices=PeriodicTimetableItem.RepeatType.choices,
        default=PeriodicTimetableItem.RepeatType.Weekly,
        max_length=1,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='periodic_event_details'
    )


class NonPeriodicEventDetails(EventDetails):
    """Represent details for non-periodic course events."""
    date = models.DateTimeField()
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='non_periodic_event_details'
    )
