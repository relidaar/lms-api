from config.views import MultiSerializerViewSet, UUIDLookupFieldMixin
from lms_core.models import Course, StudentGroup, Timetable, PeriodicEvent, NonPeriodicEvent, EventType
from lms_core.serializers import CourseSerializer, EventTypeSerializer, NonPeriodicEventSerializer, \
    PeriodicEventSerializer, TimetableSerializer, StudentGroupSerializer


class CourseViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }
    filterset_fields = ('code', 'title', 'instructors', 'student_groups',)
    search_fields = ('code', 'title',)


class StudentGroupViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }
    filterset_fields = ('code', 'students',)
    search_fields = ('code',)


class TimetableViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }
    filterset_fields = ('code', 'title', 'course', 'course__code',
                        'course__title', 'start_date', 'end_date',)
    search_fields = ('code', 'title',)


class EventViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    filterset_fields = ('title', 'start_time', 'end_time', 'students',
                        'instructor', 'instructor__user__full_name', 'instructor__user__email',
                        'timetable', 'timetable__code', 'event_type', 'event_type__title',)
    search_fields = ('title',)


class PeriodicEventViewSet(EventViewSet):
    queryset = PeriodicEvent.objects.all()
    serializers = {
        'default': PeriodicEventSerializer,
    }
    filterset_fields = EventViewSet.filterset_fields + \
        ('weekday', 'repeat_type',)


class NonPeriodicEventViewSet(EventViewSet):
    queryset = NonPeriodicEvent.objects.all()
    serializers = {
        'default': NonPeriodicEventSerializer,
    }
    filterset_fields = EventViewSet.filterset_fields + \
        ('date',)


class EventTypeViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
    filterset_fields = ('title',)
    search_fields = ('title',)
