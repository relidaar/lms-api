from config.views import MultiSerializerViewSet, UUIDViewSet
from lms_core.models import Course, StudentGroup, Timetable, PeriodicEvent, NonPeriodicEvent, EventType
from lms_core.serializers import CourseSerializer, EventTypeSerializer, NonPeriodicEventSerializer, \
    PeriodicEventSerializer, TimetableSerializer, StudentGroupSerializer


class CourseViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }


class StudentGroupViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }


class TimetableViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }


class PeriodicEventViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = PeriodicEvent.objects.all()
    serializers = {
        'default': PeriodicEventSerializer,
    }


class NonPeriodicEventViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = NonPeriodicEvent.objects.all()
    serializers = {
        'default': NonPeriodicEventSerializer,
    }


class EventTypeViewSet(MultiSerializerViewSet, UUIDViewSet):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
