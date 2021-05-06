from rest_framework import viewsets, mixins
from rest_framework.viewsets import ModelViewSet
from django_auto_prefetching import AutoPrefetchViewSetMixin

from config.views import MultiSerializerMixin, UUIDLookupFieldMixin
from lms_core.models import (
    Course, Event, Request, Response, StudentGroup, Timetable, EventType
)
from lms_core.serializers import (
    EventSerializer, CourseSerializer, EventTypeSerializer, RequestSerializer,
    ResponseSerializer, TimetableSerializer, StudentGroupSerializer
)


class RequestViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, AutoPrefetchViewSetMixin):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filterset_fields = ('created_date', 'created_by',)


class ResponseViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, AutoPrefetchViewSetMixin):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    filterset_fields = ('status', 'created_date', 'created_by',)


class CourseViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }
    filterset_fields = ('code', 'title', 'instructors', 'student_groups',)
    search_fields = ('code', 'title',)


class StudentGroupViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }
    filterset_fields = ('code', 'students',)
    search_fields = ('code',)


class TimetableViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }
    filterset_fields = ('code', 'title', 'course', 'course__code',
                        'course__title', 'start_date', 'end_date',)
    search_fields = ('code', 'title',)


class EventViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Event.objects.all()
    filterset_fields = ('title', 'event_type', 'event_type__title', 'timetable',
                        'timetable__code',)

    search_fields = ('title',)
    serializers = {
        'default': EventSerializer,
    }


class EventTypeViewSet(ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
    filterset_fields = ('title',)
    search_fields = ('title',)
