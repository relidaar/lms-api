import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model


class UUIDFieldMixin(models.Model):
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier'
    )

    class Meta:
        abstract = True


class Content(UUIDFieldMixin, models.Model):
    """Basic model for course contents."""
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file',
            )
        },
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class ContentItem(UUIDFieldMixin, models.Model):
    """Basic model for content items."""
    owner = models.ForeignKey(
        get_user_model(),
        related_name='%(class)s_related',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ContentItem):
    content = models.TextField()


class File(ContentItem):
    file = models.FileField(upload_to='files')


class Image(ContentItem):
    file = models.FileField(upload_to='images')


class Video(ContentItem):
    url = models.URLField()
