from typing import TYPE_CHECKING
import itertools

from django.shortcuts import render
from rest_framework import viewsets, serializers, status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Tag, Directory
from .serializers import PostSerializer, TagSerializer, DirectorySerializer

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

    def create(self, request, *args, **kwargs):
        usr: User = request.user
        request.data['author'] = usr.id
        tag_names = request.data['tags']
        tags = map(_get_tag_with_name, tag_names)

        avail_tags, un_avail_names, un_avail_tags = list(), list(), None
        for tag, t_name in zip(tags, tag_names):
            if tag is None:
                avail_tags.append(tag)
            else:
                un_avail_names.append(t_name)
        un_avail_tags = (Tag(name) for name in tag_names)
        Tag.objects.bulk_create(un_avail_tags)

        request.data['tags']: List[Tag] = map(lambda t: t.uuid, itertools.chain(avail_tags, un_avail_tags))
        Tag.objects.bulk_create(request.data['tags'])
        request.data['tags'] = None
        return super(PostViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.reading += 1
        serialize = PostSerializer(post)
        if serialize.is_valid():
            post.save()
            return Response(serialize.data, 200)
        else:
            return Response(serialize.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class TagReadViewSet(viewsets.GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """
    Tag view SET
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # 注入 request 属性
        context['request'] = self.request
        return context
