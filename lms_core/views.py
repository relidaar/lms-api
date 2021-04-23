from config.views import MultiSerializerViewSet, UUIDLookupFieldMixin
from lms_core.models import Course, StudentGroup, Timetable, PeriodicEvent, NonPeriodicEvent, EventType
from lms_core.serializers import CourseSerializer, EventTypeSerializer, NonPeriodicEventSerializer, \
    PeriodicEventSerializer, TimetableSerializer, StudentGroupSerializer


class CourseViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }


class StudentGroupViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }


class TimetableViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }


class PeriodicEventViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = PeriodicEvent.objects.all()
    serializers = {
        'default': PeriodicEventSerializer,
    }


class NonPeriodicEventViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = NonPeriodicEvent.objects.all()
    serializers = {
        'default': NonPeriodicEventSerializer,
    }


class EventTypeViewSet(MultiSerializerViewSet, UUIDLookupFieldMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
