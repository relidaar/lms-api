from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from generic_relations.relations import GenericRelatedField

from lms_core.models import Course, Request, Response, StudentGroup, Timetable, EventType, PeriodicEvent, NonPeriodicEvent
from accounts.models import InstructorProfile, StudentProfile


class RequestSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='uuid', queryset=get_user_model().objects.all())
    requested_object = GenericRelatedField({
        Course: serializers.SlugRelatedField(slug_field='uuid', queryset=Course.objects.all()),
        StudentGroup: serializers.SlugRelatedField(slug_field='uuid', queryset=StudentGroup.objects.all()),
        Timetable: serializers.SlugRelatedField(slug_field='uuid', queryset=Timetable.objects.all()),
        PeriodicEvent: serializers.SlugRelatedField(slug_field='uuid', queryset=PeriodicEvent.objects.all()),
        NonPeriodicEvent: serializers.SlugRelatedField(slug_field='uuid', queryset=NonPeriodicEvent.objects.all()),
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


class EventSerializer(ModelSerializer):
    event_type = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=EventType.objects.all(),
    )

    instructor = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=InstructorProfile.objects.all(),
    )

    students = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=StudentProfile.objects.all(),
        many=True,
    )

    timetable = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Timetable.objects.all(),
    )

    class Meta:
        abstract = True
        fields = ('uuid', 'title', 'description', 'event_type',
                  'start_time', 'end_time', 'instructor', 'students', 'timetable',)


class PeriodicEventSerializer(EventSerializer):
    class Meta:
        model = PeriodicEvent
        fields = EventSerializer.Meta.fields + ()


class NonPeriodicEventSerializer(EventSerializer):
    class Meta:
        model = NonPeriodicEvent
        fields = EventSerializer.Meta.fields + ()


class EventTypeSerializer(ModelSerializer):
    class Meta:
        model = EventType
        fields = ('uuid', 'title',)
