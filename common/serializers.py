from rest_framework import serializers


class UUIDHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    lookup_field = 'uuid'
