# import typing

from .models import Post, Tag, Directory, User
# from . import logger

# from django.db.models import Q
from rest_framework import serializers
# from rest_framework_recursive.fields import RecursiveField
# from rest_framework.decorators import action, detail_route

# if typing.TYPE_CHECKING:
#     from rest_framework.serializers import BaseSerializer


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
    if embed_fields is not None and keyword in embed_fields.replace(' ', '').split(','):
        serializer.fields[keyword] = serialize_cls(read_only=readonly,
                                                   context=context, many=many,
                                                   validators=validators)


class TagSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TagSerializer, self).__init__(*args, **kwargs)
        # request = kwargs['context']['request']
        # 应该是级联请求产生的
        # handle_embeds(self, request, 'post', PostSerializer, kwargs['context'],
        #               readonly=True, many=True)

    class Meta:
        model = Tag
        fields = ('tag_name', 'uuid', 'related_posts')
        read_only_fields = ('uuid', 'related_posts')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all(),
                                          allow_null=False, required=True)
    tags = serializers.SlugRelatedField(slug_field='uuid', read_only=True, allow_null=True)
    # tags = serializers.ManyRelatedField()

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']

        handle_embeds(self, request, 'tags', TagSerializer, kwargs['context'],
                      readonly=True, many=True)
        handle_embeds(self, request, 'directory', DirectorySerializer,
                      kwargs['context'], readonly=True, many=True)

        if request.method == "POST":
            # TODO: add validation for this field.
            # self.validators.append()
            self.fields['directory'] = \
                serializers.SlugRelatedField(slug_field='id', queryset=Directory.objects,
                                             allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'author', 'reading', 'tags')


class DirectorySerializer(serializers.ModelSerializer):

    def get_father_directory(self, obj):
        if obj.father_directory is None:
            return None
        return DirectorySerializer(obj.father_directory, context=self.context)

    def get_child_directories(self, obj):
        return DirectorySerializer(obj.child_directories.all(), context=self.context, many=True).data

    def __init__(self, *args, **kwargs):
        super(DirectorySerializer, self).__init__(*args, **kwargs)
        try:
            request = kwargs['context']['request']
            if request.method == "GET":
                # handle_embeds(self, request, 'father_directory', serializers.PrimaryKeyRelatedField,
                #               kwargs['context'], readonly=True)
                embed = request.query_params.get('embed', None)
                if embed is None:
                    return
                embeds = embed.replace(' ', '').split(',')
                if 'father_directory' in embeds:
                    self.fields['father_directory'] = serializers.PrimaryKeyRelatedField(read_only=True)
                if 'child_directories' in embeds:
                    self.fields['child_directories'] = serializers.SerializerMethodField(allow_null=True)
                handle_embeds(self, request, 'posts', PostSerializer,
                              kwargs['context'], readonly=True, many=True)
            elif request.method == "POST":
                # TODO: add validation for this field.
                # self.validators.append()
                self.fields['father_directory'] = \
                    serializers.SlugRelatedField(slug_field='uuid', queryset=Directory.objects,
                                                 allow_null=True, required=False)
        except KeyError as e:
            print("no attr")
        finally:
            return

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
