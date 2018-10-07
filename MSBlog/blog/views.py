from typing import TYPE_CHECKING
import itertools

from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Tag, Directory
from .serializers import PostSerializer, TagSerializer, DirectorySerializer, PostListSerialize, PostViewSerializer

if TYPE_CHECKING:
    from .models import User
    from typing import List

INIT_CTX_FIELDS = ('GET', )


def _get_tag_with_name(tag_name: str)->Tag:
    raise NotImplemented("_get_tag_with_name un impl.")


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """
    博客的VIEWSET
    """
    queryset = Post.objects.all().order_by('created_time')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('uuid',)

    @action(methods=['GET'], detail=True)
    def tags(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        tags = post.tags
        serializers = TagSerializer(tags, many=True)
        return Response(serializers.data)

    def create(self, request, *args, **kwargs):
        usr: User = request.user
        request.data['author'] = usr.id
        tag_names = request.data['tags']
        tag_ids = []
        # fill abstract data default
        if getattr(request.data, 'abstract', None) is None:
            request.data['abstract'] = request.data['content'][:50]
        for tag_name in tag_names:
            # cur_tag = get_object_or_404(Tag.objects, tag_name=tag_name)
            try:
                cur_tag = Tag.objects.get(tag_name=tag_name)
            except Tag.DoesNotExist:
                cur_tag = None

            if cur_tag is None:
                # create a new tag
                cur_tag = Tag(tag_name=tag_name)
            cur_tag.related_posts += 1
            # wtf?
            cur_tag.save()
            tag_ids.append(cur_tag.pk)
        request.data['tags'] = tag_ids

        return super(PostViewSet, self).create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerialize
        elif self.action == 'retrieve':
            return PostViewSerializer
        return PostSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            post.reading += 1
            serialize = PostSerializer(post)
            post.save()
            return Response(serialize.data, 200)
        except Post.DoesNotExist:
            raise Http404


class RelatedTagPostViewSet(viewsets.GenericViewSet, ListModelMixin):
    model = Post
    serializer_class = PostListSerialize

    def get_queryset(self):
        tag_uid = self.kwargs['tag_uuid']
        try:
            tag = Tag.objects.get(uuid=tag_uid)
            return tag.posts.all()
        except Tag.DoesNotExist:
            raise Http404



class TagReadViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    Tag view SET
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tag_name', )

    # @action(methods=['GET'], detail=True)
    # def posts(self, request, pk=None):
    #     try:
    #         tag = Tag.objects.get(pk=pk)
    #         posts = tag.posts
    #         serializers = PostListSerialize(posts, many=True)
    #         return Response(serializers.data)
    #     except Tag.DoesNotExist:
    #         raise Http404

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # 注入 request 属性
        context['request'] = self.request


class TagCreateViewSet(viewsets.ModelViewSet, CreateModelMixin):
    """
    Tag view SET
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class DirectoryViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    目录的viewset
    """
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=['GET'], detail=True)
    def get_child_dirs(self, request, pk=None):
        dir: Directory = self.queryset.get(pk=pk)
        serializer = DirectorySerializer(dir.child_directories, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # 注入 request 属性
        context['request'] = self.request
        return context


@api_view(['GET'])
def get_root_directories(request):
    """
    获取所有没有父对象的目录
    :return:
    """
    objects = Directory.objects.filter(father_directory__isnull=True)
    serializer = DirectorySerializer(objects, many=True)
    return Response(serializer.data)