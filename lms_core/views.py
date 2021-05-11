from rest_framework import viewsets, mixins
from django_auto_prefetching import AutoPrefetchViewSetMixin

from common.views import MultiSerializerMixin, UUIDLookupFieldMixin
from lms_core.models import (
    Course, Event, Request, Response, StudentGroup, Timetable, EventType
)
from lms_core.serializers import (
    EventSerializer, CourseSerializer, EventTypeSerializer, RequestSerializer,
    ResponseSerializer, TimetableSerializer, StudentGroupSerializer
)
from lms_core import filters


class RequestViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, AutoPrefetchViewSetMixin):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filterset_fields = ('created_date', 'created_by',)


class ResponseViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin, AutoPrefetchViewSetMixin):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    filterset_fields = ('status', 'created_date', 'created_by',)


class CourseViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }
    filterset_class = filters.CourseFilter
    search_fields = ('code', 'title',)


class StudentGroupViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = StudentGroup.objects.all()
    serializers = {
        'default': StudentGroupSerializer,
    }
    filterset_class = filters.StudentGroupFilter
    search_fields = ('code',)


class TimetableViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }
    filterset_class = filters.TimetableFilter
    search_fields = ('code', 'title',)


class EventViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Event.objects.all()
    serializers = {
        'default': EventSerializer,
    }
    filterset_class = filters.EventFilter
    search_fields = ('title',)


class EventTypeViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
    filterset_fields = ('title',)
    search_fields = ('title',)
