from config.views import MultiSerializerViewSet, UUIDLookupFieldMixin
from lms_core.models import Course, StudentGroup, Timetable, PeriodicEvent, NonPeriodicEvent, EventType
from lms_core.serializers import CourseSerializer, EventTypeSerializer, NonPeriodicEventSerializer, \
    PeriodicEventSerializer, TimetableSerializer, StudentGroupSerializer


class CourseViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }
    filterset_fields = ('code', 'title')


class StudentGroupViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }
    filterset_fields = ('code',)


class TimetableViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }
    filterset_fields = ('code', 'title', 'course', 'start_date', 'end_date',)


class PeriodicEventViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = PeriodicEvent.objects.all()
    serializers = {
        'default': PeriodicEventSerializer,
    }
    filterset_fields = ('title', 'event_type', 'start_time', 'end_time',
                        'instructor', 'timetable', 'weekday', 'repeat_type',)


class NonPeriodicEventViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = NonPeriodicEvent.objects.all()
    serializers = {
        'default': NonPeriodicEventSerializer,
    }
    filterset_fields = ('title', 'event_type', 'start_time', 'end_time',
                        'instructor', 'timetable', 'date',)


class EventTypeViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
    filterset_fields = ('title',)
