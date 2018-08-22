from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .models import Post, Tag, Directory
from .serializers import PostSerializer, TagSerializer, DirectorySerializer


INIT_CTX_FIELDS = ('GET', )


# Create your views here.
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    博客的VIEWSET
    """
    queryset = Post.objects.all().order_by('created_time')
    serializer_class = PostSerializer


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


class DirectoryViewSet(viewsets.ModelViewSet):
    """
    目录的viewset
    """
    queryset = Directory.objects.all().order_by('name')
    serializer_class = DirectorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # 注入 request 属性
        # context['request'] = self.request
        return {'request': self.request}
