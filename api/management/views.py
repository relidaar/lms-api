from django_auto_prefetching import AutoPrefetchViewSetMixin
from rest_framework import viewsets, mixins

from api.common.views import UUIDLookupFieldMixin
from api.management.serializers import RequestSerializer, ResponseSerializer
from management.models import Request, Response


class RequestViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin,
                     AutoPrefetchViewSetMixin):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filterset_fields = ('created_date', 'created_by',)


class ResponseViewSet(UUIDLookupFieldMixin, viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin,
                      AutoPrefetchViewSetMixin):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    filterset_fields = ('status', 'created_date', 'created_by',)
