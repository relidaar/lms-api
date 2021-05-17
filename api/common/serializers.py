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
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }


class TextContentItemSerializer(ContentItemSerializer):
    class Meta(ContentItemSerializer.Meta):
        model = TextContentItem
        fields = ContentItemSerializer.Meta.fields + ('content',)
        extra_kwargs = ContentItemSerializer.Meta.extra_kwargs


class FileContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = FileContentItem
        fields = ContentItemSerializer.Meta.fields + ('file',)
        extra_kwargs = ContentItemSerializer.Meta.extra_kwargs


class ImageContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = ImageContentItem
        fields = ContentItemSerializer.Meta.fields + ('file',)
        extra_kwargs = ContentItemSerializer.Meta.extra_kwargs


class VideoContentItemSerializer(ContentItemSerializer):
    class Meta:
        model = VideoContentItem
        fields = ContentItemSerializer.Meta.fields + ('url',)
        extra_kwargs = ContentItemSerializer.Meta.extra_kwargs


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
        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid',
            }
        }
