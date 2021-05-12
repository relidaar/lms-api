from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from common.models import UUIDFieldMixin


class Request(UUIDFieldMixin, models.Model):
    """Represent a permission request."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    requested_object = GenericForeignKey('content_type', 'object_id',)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )


class Response(UUIDFieldMixin, models.Model):
    """Represent a permission response."""
    class RequestStatus(models.TextChoices):
        InProcessing = 'P', _('InProcessing')
        Approved = 'A', _('Approved')
        Declined = 'D', _('Declined')

    status = models.CharField(
        max_length=1,
        choices=RequestStatus.choices,
        default=RequestStatus.InProcessing
    )
    related_request = models.OneToOneField(Request, on_delete=models.CASCADE)
    comment = models.TextField(blank=True,)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )
