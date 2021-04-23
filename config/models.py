import uuid

from django.db import models


class UUIDFieldMixin(models.Model):
    uuid = models.UUIDField(unique=True, editable=False,
                            default=uuid.uuid4, verbose_name='Public identifier')

    class Meta:
        abstract = True
