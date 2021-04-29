from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from accounts.models import InstructorProfile, StudentProfile
from config.models import UUIDFieldMixin


class Request(UUIDFieldMixin, models.Model):
    """Represent a permission request."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    requested_object = GenericForeignKey('content_type', 'object_id',)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                   null=True,)


class Response(UUIDFieldMixin, models.Model):
    """Represent a permission response."""
    class RequestStatus(models.TextChoices):
        InProcessing = 'P', _('InProcessing')
        Approved = 'A', _('Approved')
        Declined = 'D', _('Declined')

    status = models.CharField(max_length=1, choices=RequestStatus.choices,
                              default=RequestStatus.InProcessing)
    related_request = models.OneToOneField(Request, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                                   null=True,)


class StudentGroup(UUIDFieldMixin, models.Model):
    """Represent an academic group of students."""
    code = models.CharField(max_length=10, unique=True)
    students = models.ManyToManyField(StudentProfile)

    def __str__(self):
        return self.code


class Course(UUIDFieldMixin, models.Model):
    """Represent an academic course."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    syllabus = models.TextField(blank=True)
    instructors = models.ManyToManyField(
        InstructorProfile, related_name='instructors')
    student_groups = models.ManyToManyField(StudentGroup)

    def __str__(self):
        return f'{self.code} - {self.title}'


class Timetable(UUIDFieldMixin, models.Model):
    """Represent an event timetable related to specific course."""
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255, blank=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='timetables')
    start_date = models.DateField(verbose_name='Course start date')
    end_date = models.DateField(verbose_name='Course end date')

    def __str__(self):
        return f'{self.title} ({self.course.code} course)'


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

    weekday = models.CharField(
        max_length=2, choices=WeekDay.choices, default=WeekDay.Monday)
    repeat_type = models.CharField(
        max_length=1, choices=RepeatType.choices, default=RepeatType.Weekly)
