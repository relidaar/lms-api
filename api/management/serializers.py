from django.contrib.auth import get_user_model
from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from accounts.models import StudentGroup
from api.common.serializers import UUIDHyperlinkedRelatedField
from education.models import (
    Course,
    Event,
    EventType,
    Timetable,
)
from management.models import Request, Response


class RequestSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UUIDHyperlinkedRelatedField(
        view_name='user-detail',
        queryset=get_user_model().objects.all(),
    )

    requested_object = GenericRelatedField({
        Course: UUIDHyperlinkedRelatedField(
            view_name='course-detail',
            queryset=Course.objects.all(),
        ),
        StudentGroup: UUIDHyperlinkedRelatedField(
            view_name='student-group-detail',
            queryset=StudentGroup.objects.all(),
        ),
        Timetable: UUIDHyperlinkedRelatedField(
            view_name='timetable-detail',
            queryset=Timetable.objects.all(),
        ),
        Event: UUIDHyperlinkedRelatedField(
            view_name='event-detail',
            queryset=Event.objects.all(),
        ),
        EventType: UUIDHyperlinkedRelatedField(
            view_name='event-type-detail',
            queryset=EventType.objects.all(),
        ),
    })

    class Meta:
        model = Request
        fields = (
            'url', 'uuid', 'created_date', 'created_by', 'requested_object',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UUIDHyperlinkedRelatedField(
        view_name='user-detail',
        queryset=get_user_model().objects.all(),
    )

    related_request = UUIDHyperlinkedRelatedField(
        view_name='request-detail',
        queryset=Request.objects.all(),
    )

    class Meta:
        model = Response
        fields = (
            'url', 'uuid', 'status', 'created_date', 'created_by',
            'related_request', 'comment',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }
