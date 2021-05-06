from django.contrib.auth import get_user_model
from django.contrib.contenttypes import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from generic_relations.relations import GenericRelatedField

from lms_core.models import (
    Course, Event, NonPeriodicEventDetails, PeriodicEventDetails, Request, Response,
    StudentGroup, Timetable, EventType,
)
from accounts.models import InstructorProfile, StudentProfile


class RequestSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='uuid', queryset=get_user_model().objects.all())
    requested_object = GenericRelatedField({
        Course: serializers.SlugRelatedField(slug_field='uuid', queryset=Course.objects.all()),
        StudentGroup: serializers.SlugRelatedField(slug_field='uuid', queryset=StudentGroup.objects.all()),
        Timetable: serializers.SlugRelatedField(slug_field='uuid', queryset=Timetable.objects.all()),
        Event: serializers.SlugRelatedField(slug_field='uuid', queryset=Event.objects.all()),
        EventType: serializers.SlugRelatedField(slug_field='uuid', queryset=EventType.objects.all()),
    })

    class Meta:
        model = Request
        fields = ('uuid', 'created_date', 'created_by', 'requested_object',)


class ResponseSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='uuid', queryset=get_user_model().objects.all())
    related_request = serializers.SlugRelatedField(
        slug_field='uuid', queryset=Request.objects.all()
    )

    class Meta:
        model = Response
        fields = ('uuid', 'status', 'created_date', 'created_by',
                  'related_request', 'comment',)


class CourseSerializer(ModelSerializer):
    instructors = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=InstructorProfile.objects.all(),
        many=True,
    )

    student_groups = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=StudentGroup.objects.all(),
        many=True,
    )

    class Meta:
        model = Course
        fields = ('uuid', 'code', 'title', 'syllabus',
                  'instructors', 'student_groups',)


class StudentGroupSerializer(ModelSerializer):
    students = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=StudentProfile.objects.all(),
        many=True,
    )

    class Meta:
        model = StudentGroup
        fields = ('uuid', 'code', 'students',)


class TimetableSerializer(ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Timetable
        fields = ('uuid', 'code', 'title', 'course', 'start_date', 'end_date',)


class EventDetailsSerializer(ModelSerializer):
    instructor = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=InstructorProfile.objects.all(),
    )

    students = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=StudentProfile.objects.all(),
        many=True,
    )

    class Meta:
        abstract = True
        fields = ('uuid', 'start_time', 'end_time', 'instructor', 'students',)


class PeriodicEventDetailsSerializer(EventDetailsSerializer):
    class Meta:
        model = PeriodicEventDetails
        fields = EventDetailsSerializer.Meta.fields + \
            ('weekday', 'repeat_type',)


class NonPeriodicEventDetailsSerializer(EventDetailsSerializer):
    class Meta:
        model = NonPeriodicEventDetails
        fields = EventDetailsSerializer.Meta.fields + \
            ('date',)


class EventSerializer(ModelSerializer):
    event_type = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=EventType.objects.all(),
    )

    periodic_event_details = PeriodicEventDetailsSerializer(
        source='periodic_event_details_set',
        many=True,
    )
    non_periodic_event_details = NonPeriodicEventDetailsSerializer(
        source='non_periodic_event_details_set',
        many=True,
    )

    timetable = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Timetable.objects.all(),
    )

    class Meta:
        model = Event
        depth = 1
        fields = ('uuid', 'title', 'description', 'event_type', 'timetable',
                  'periodic_event_details', 'non_periodic_event_details')


class EventTypeSerializer(ModelSerializer):
    class Meta:
        model = EventType
        fields = ('uuid', 'title',)
