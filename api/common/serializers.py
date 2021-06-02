from generic_relations.relations import GenericRelatedField
from rest_framework import serializers

from common.models import (
    FileContentItem,
    ImageContentItem,
    TextContentItem,
    VideoContentItem,
)


class UUIDHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    lookup_field = 'uuid'


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ('uuid', 'title', 'created_at', 'updated_at',)


class TextContentItemSerializer(ContentItemSerializer):
    class Meta(ContentItemSerializer.Meta):
        model = TextContentItem
        fields = ContentItemSerializer.Meta.fields + ('content',)


class FileContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = FileContentItem
        fields = ContentItemSerializer.Meta.fields + ('file',)


class ImageContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = ImageContentItem
        fields = ContentItemSerializer.Meta.fields + ('file',)


class VideoContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = VideoContentItem
        fields = ContentItemSerializer.Meta.fields + ('url',)


class ContentSerializer(serializers.ModelSerializer):
    item = GenericRelatedField({
        TextContentItem: TextContentItemSerializer(),
        FileContentItem: FileContentItemSerializer(),
        ImageContentItem: ImageContentItemSerializer(),
        VideoContentItem: VideoContentItemSerializer(),
    })

    class Meta:
        abstract = True
        fields = ('uuid', 'item',)
