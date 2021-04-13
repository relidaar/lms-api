import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import InstructorProfile, StudentProfile


class StudentGroup(models.Model):
    """Represent an academic group of students."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    code = models.CharField(max_length=10, unique=True)
    students = models.ManyToManyField(StudentProfile)

    def __str__(self):
        return self.code


class Course(models.Model):
    """Represent an academic course."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    syllabus = models.TextField(blank=True)
    instructors = models.ManyToManyField(InstructorProfile, related_name='instructors')
    student_groups = models.ManyToManyField(StudentGroup)

    def __str__(self):
        return f'{self.code} - {self.title}'


class Timetable(models.Model):
    """Represent an event timetable related to specific course."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    start_date = models.DateField(verbose_name='Course start date')
    end_date = models.DateField(verbose_name='Course end date')

    def __str__(self):
        return f'{self.title} ({self.course.code} course)'


class EventType(models.Model):
    """Represent types of timetable events."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Event(models.Model):
    """Basic model for timetable events."""
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    start_time = models.TimeField(verbose_name='Event start time')
    end_time = models.TimeField(verbose_name='Event end time')
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    students = models.ManyToManyField(StudentProfile)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.event_type.title})'

    class Meta:
        abstract = True


class NonPeriodicEvent(Event):
    """Represent non periodic event with specific date."""
    date = models.DateField()


class PeriodicEvent(Event):
    """Represent periodic event with specific weekday and repeat type."""
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

    weekday = models.CharField(max_length=2, choices=WeekDay.choices, default=WeekDay.Monday)
    repeat_type = models.CharField(max_length=1, choices=RepeatType.choices, default=RepeatType.Weekly)
