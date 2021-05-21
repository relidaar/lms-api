from drf_writable_nested import serializers as nested_serializers
from rest_framework import serializers

from accounts.models import InstructorProfile, StudentProfile, StudentGroup
from api.common.serializers import ContentSerializer, UUIDHyperlinkedRelatedField
from education.models import (
    Assignment,
    AssignmentContent,
    Course,
    CourseContent,
    Event,
    Grade,
    NonPeriodicEventDetails,
    PeriodicEventDetails,
    Solution,
    SolutionContent,
    Timetable,
    EventType,
)


class CourseContentSerializer(ContentSerializer):
    class Meta:
        model = CourseContent
        fields = ContentSerializer.Meta.fields + ()


class AssignmentContentSerializer(ContentSerializer):
    class Meta:
        model = AssignmentContent
        fields = ContentSerializer.Meta.fields + ()


class SolutionContentSerializer(ContentSerializer):
    class Meta:
        model = SolutionContent
        fields = ContentSerializer.Meta.fields + ()


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

    contents = CourseContentSerializer(many=True, required=False, )

    class Meta:
        model = Course
        fields = (
            'url', 'uuid', 'code', 'title', 'syllabus', 'instructors',
            'student_groups', 'timetables', 'contents',
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

    assignments = UUIDHyperlinkedRelatedField(
        view_name='assignment-detail',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Timetable
        fields = (
            'url', 'uuid', 'code', 'title', 'course', 'start_date', 'end_date',
            'assignments',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class TimetableItemSerializer(serializers.HyperlinkedModelSerializer):
    timetable = UUIDHyperlinkedRelatedField(
        view_name='timetable-detail',
        queryset=Timetable.objects.all(),
    )

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
        fields = (
            'url', 'uuid', 'title', 'description', 'start_time', 'end_time',
            'timetable', 'instructor', 'students',
        )


class PeriodicTimetableItemSerializer(TimetableItemSerializer):
    class Meta:
        fields = TimetableItemSerializer.Meta.fields + (
            'weekday', 'repeat_type',
        )


class NonPeriodicTimetableItemSerializer(TimetableItemSerializer):
    class Meta:
        fields = TimetableItemSerializer.Meta.fields + ('date',)


class AssignmentSerializer(NonPeriodicTimetableItemSerializer):
    solutions = UUIDHyperlinkedRelatedField(
        view_name='assignment-detail',
        read_only=True,
        many=True,
    )

    contents = AssignmentContentSerializer(many=True, )

    class Meta:
        model = Assignment
        fields = NonPeriodicTimetableItemSerializer.Meta.fields + (
            'solutions', 'contents',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    assignment = UUIDHyperlinkedRelatedField(
        view_name='assignment-detail',
        queryset=Assignment.objects.all(),
    )

    student = UUIDHyperlinkedRelatedField(
        view_name='student-detail',
        queryset=StudentProfile.objects.all(),
    )

    grades = UUIDHyperlinkedRelatedField(
        view_name='grade-detail',
        read_only=True,
        many=True,
    )

    contents = SolutionContentSerializer(many=True, )

    class Meta:
        model = Solution
        fields = (
            'url', 'uuid', 'assignment', 'student', 'created_at', 'comment',
            'grades', 'contents',
        )


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    solution = UUIDHyperlinkedRelatedField(
        view_name='solution-detail',
        queryset=Solution.objects.all(),
    )

    instructor = UUIDHyperlinkedRelatedField(
        view_name='instructor-detail',
        queryset=InstructorProfile.objects.all(),
    )

    class Meta:
        model = Grade
        fields = (
            'url', 'uuid', 'value', 'solution', 'instructor', 'created_at',
            'comment',
        )


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


class EventSerializer(serializers.HyperlinkedModelSerializer, nested_serializers.NestedCreateMixin,
                      nested_serializers.NestedUpdateMixin):
    event_type = UUIDHyperlinkedRelatedField(
        view_name='event-type-detail',
        queryset=EventType.objects.all(),
    )

    periodic_event_details = PeriodicEventDetailsSerializer(many=True, )
    non_periodic_event_details = NonPeriodicEventDetailsSerializer(many=True, )

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
