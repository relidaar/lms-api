from rest_framework import serializers
from drf_writable_nested import serializers as nested_serializers

from education.models import (
    Course,
    Event,
    NonPeriodicEventDetails,
    PeriodicEventDetails,
    Timetable,
    EventType,
)
from accounts.models import InstructorProfile, StudentProfile, StudentGroup
from api.common.serializers import UUIDHyperlinkedRelatedField


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    instructors = UUIDHyperlinkedRelatedField(
        view_name='instructor-detail',
        queryset=InstructorProfile.objects.all(),
        many=True,
    )

    student_groups = UUIDHyperlinkedRelatedField(
        view_name='student-group-detail',
        queryset=StudentGroup.objects.all(),
        many=True,
    )

    timetables = UUIDHyperlinkedRelatedField(
        view_name='timetable-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Course
        fields = (
            'url', 'uuid', 'code', 'title', 'syllabus', 'instructors',
            'student_groups', 'timetables',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class TimetableSerializer(serializers.HyperlinkedModelSerializer):
    course = UUIDHyperlinkedRelatedField(
        view_name='course-detail',
        queryset=Course.objects.all(),
    )

    events = UUIDHyperlinkedRelatedField(
        view_name='event-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Timetable
        fields = (
            'url', 'uuid', 'code', 'title', 'course', 'start_date', 'end_date',
            'events',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class EventDetailsSerializer(serializers.ModelSerializer):
    instructor = UUIDHyperlinkedRelatedField(
        view_name='instructor-detail',
        queryset=InstructorProfile.objects.all(),
    )

    students = UUIDHyperlinkedRelatedField(
        view_name='student-detail',
        queryset=StudentProfile.objects.all(),
        many=True,
    )

    class Meta:
        abstract = True
        fields = ('uuid', 'start_time', 'end_time', 'instructor', 'students',)


class PeriodicEventDetailsSerializer(EventDetailsSerializer):
    class Meta:
        model = PeriodicEventDetails
        fields = EventDetailsSerializer.Meta.fields + (
            'weekday', 'repeat_type',
        )


class NonPeriodicEventDetailsSerializer(EventDetailsSerializer):
    class Meta:
        model = NonPeriodicEventDetails
        fields = EventDetailsSerializer.Meta.fields + ('date',)


class EventSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.NestedCreateMixin, nested_serializers.NestedUpdateMixin):
    event_type = UUIDHyperlinkedRelatedField(
        view_name='event-type-detail',
        queryset=EventType.objects.all(),
    )

    periodic_event_details = PeriodicEventDetailsSerializer(many=True,)
    non_periodic_event_details = NonPeriodicEventDetailsSerializer(many=True,)

    timetable = UUIDHyperlinkedRelatedField(
        view_name='timetable-detail',
        queryset=Timetable.objects.all(),
    )

    class Meta:
        model = Event
        depth = 1
        fields = (
            'url', 'uuid', 'title', 'description', 'event_type', 'timetable',
            'periodic_event_details', 'non_periodic_event_details',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('url', 'uuid', 'title',)
        extra_kwargs = {
            'url': {
                'view_name': 'event-type-detail',
                'lookup_field': 'uuid',
            }
        }
