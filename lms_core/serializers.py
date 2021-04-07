from rest_framework.serializers import ModelSerializer

from lms_core.models import Course, StudentGroup, Timetable, EventType, PeriodicEvent, NonPeriodicEvent


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class StudentGroupSerializer(ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = '__all__'


class TimetableSerializer(ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'


class PeriodicEventSerializer(ModelSerializer):
    class Meta:
        model = PeriodicEvent
        fields = '__all__'


class NonPeriodicEventSerializer(ModelSerializer):
    class Meta:
        model = NonPeriodicEvent
        fields = '__all__'


class EventTypeSerializer(ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'
