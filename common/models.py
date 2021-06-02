import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class TextContentItem(ContentItem):
    content = models.TextField()


class FileContentItem(ContentItem):
    file = models.FileField(upload_to='files')


class ImageContentItem(ContentItem):
    file = models.FileField(upload_to='images')


class VideoContentItem(ContentItem):
    url = models.URLField()
