from rest_framework.viewsets import ModelViewSet


class UUIDViewSet(ModelViewSet):
    lookup_field = 'uuid'


class MultiSerializerViewSet(ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])