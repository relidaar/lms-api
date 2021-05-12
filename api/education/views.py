from rest_framework import viewsets, mixins
from django_auto_prefetching import AutoPrefetchViewSetMixin

from api.common.views import MultiSerializerMixin, UUIDLookupFieldMixin
from education.models import (
    Course,
    Event,
    Timetable,
    EventType,
)
from api.education.serializers import (
    EventSerializer,
    CourseSerializer,
    EventTypeSerializer,
    TimetableSerializer,
)
from api.education.filters import CourseFilter, EventFilter, TimetableFilter


class CourseViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Course.objects.all()
    serializers = {
        'default': CourseSerializer,
    }
    filterset_class = CourseFilter
    search_fields = ('code', 'title',)


class TimetableViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Timetable.objects.all()
    serializers = {
        'default': TimetableSerializer,
    }
    filterset_class = TimetableFilter
    search_fields = ('code', 'title',)


class EventViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = Event.objects.all()
    serializers = {
        'default': EventSerializer,
    }
    filterset_class = EventFilter
    search_fields = ('title',)


class EventTypeViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin, AutoPrefetchViewSetMixin):
    queryset = EventType.objects.all()
    serializers = {
        'default': EventTypeSerializer,
    }
    filterset_fields = ('title',)
    search_fields = ('title',)
