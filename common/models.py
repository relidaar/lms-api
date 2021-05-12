import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDFieldMixin(models.Model):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier'
    )

    class Meta:
        abstract = True
