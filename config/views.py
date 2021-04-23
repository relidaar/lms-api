from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet


class UUIDLookupFieldMixin(mixins.RetrieveModelMixin):
    lookup_field = 'uuid'


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
