import typing

from .models import Post, Tag, Directory
from . import logger

from django.db.models import Q
from rest_framework import serializers

if typing.TYPE_CHECKING:
    from rest_framework.serializers import BaseSerializer, ModelSerializer


def handle_embeds(serializer, request, keyword: str, serialize_cls: 'BaseSerializer',
                  context, validators=None, readonly=False, many=False):
    """
    :param serializer:
    :param request:
    :param keyword:
    :param serializeCls:
    :param context:
    :param readonly:
    :param many:
    :return:
    """
    embed_fields: str = request.query_params.get('embed', None)
    # 怎么处理 url 编码
    if embed_fields is not None and 'post' in embed_fields.split(','):
        serializer.fields['posts'] = serialize_cls(read_only=readonly,
                                                   context=context, many=many,
                                                   validators=validators)


class TagSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TagSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']

        handle_embeds(self, request, 'post', PostSerializer, kwargs['context'],
                      readonly=True, many=True)

    class Meta:
        model = Tag
        fields = ('tag_name', 'uuid')
        read_only_fields = ('uuid', )


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.RelatedField()
    # tags = serializers.StringRelatedField(many=True)
    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']

        handle_embeds(self, request, 'tags', TagSerializer, kwargs['context'],
                      readonly=True, many=True)
        handle_embeds(self, request, 'directories', DirectorySerializer,
                      kwargs['context'], readonly=True, many=True)

    class Meta:
        model = Post
        fields = ('title', 'author', 'reading', 'tags')


class DirectorySerializer(serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):
        super(DirectorySerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        if request.method == "GET":
            handle_embeds(self, request, 'father_directory', DirectorySerializer, kwargs['context'],
                          readonly=True, many=True)
            handle_embeds(self, request, 'directories', DirectorySerializer,
                          kwargs['child_directories'], readonly=True, many=True)
            handle_embeds(self, request, 'posts', PostSerializer,
                          kwargs['posts'], readonly=True, many=True)
        elif request.method == "POST":
            # TODO: add validation for this field.
            # self.validators.append()
            self.fields['father_directory'] = \
                serializers.SlugRelatedField(slug_field='uuid', queryset=
                Directory.objects, allow_null=True, required=False)

    class Meta:
        model = Directory
        fields = ('name', "uuid")
        read_only_fields = ("uuid", )


def father_directory_restriction(father_dir: DirectorySerializer)->DirectorySerializer:
    if father_dir.father_directory.father_directory is father_dir.father_directory:
        # the same dir
        if father_dir.name == father_dir.father_directory.name:
            raise serializers.ValidationError("the created dir has same father under it's father dir")
    return father_dir