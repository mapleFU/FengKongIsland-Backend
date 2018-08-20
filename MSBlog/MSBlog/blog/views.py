from django.shortcuts import render

from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """
    博客的VIEWSET
    """
    queryset = Post.objects.all().order_by('created_time')
    serializer_class = PostSerializer
