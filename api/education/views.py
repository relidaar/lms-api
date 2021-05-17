from rest_framework import viewsets, mixins
from django_auto_prefetching import AutoPrefetchViewSetMixin

from api.common.views import MultiSerializerMixin, UUIDLookupFieldMixin
from education.models import (
    Assignment,
    Course,
    Event,
    Grade,
    Solution,
    Timetable,
    EventType,
)
from api.education.serializers import (
    AssignmentSerializer,
    EventSerializer,
    CourseSerializer,
    EventTypeSerializer,
    GradeSerializer,
    SolutionSerializer,
    TimetableSerializer,
)
from api.education.filters import AssignmentFilter, CourseFilter, EventFilter, GradeFilter, SolutionFilter, TimetableFilter


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


class AssignmentViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = Assignment.objects.all()
    serializers = {
        'default': AssignmentSerializer,
    }
    filterset_class = AssignmentFilter
    search_fields = ('title',)


class SolutionViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = Solution.objects.all()
    serializers = {
        'default': SolutionSerializer,
    }
    filterset_class = SolutionFilter
    search_fields = ('title',)


class GradeViewSet(viewsets.ModelViewSet, MultiSerializerMixin, UUIDLookupFieldMixin):
    queryset = Grade.objects.all()
    serializers = {
        'default': GradeSerializer,
    }
    filterset_class = GradeFilter
    search_fields = ('title',)


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
