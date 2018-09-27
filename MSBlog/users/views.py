from hashlib import md5
import uuid

from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


def _gen_filename(username: str, filename: str) -> str:
    filename = "{}{}".format(uuid.uuid4(), filename)
    return f"image/{md5(username.encode('utf-8')).hexdigest()}:" \
           f"{md5(filename.encode('utf-8')).hexdigest()}"


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def get_upload_token(request):
    """
    根据用户获得上传
    :param request:
    :return:
    """
    file_name = request.data['file-name']
    auth = getattr(settings, "QINIU_AUTH", None)
    bucket_name = getattr(settings, "QINIU_BUCKET_NAME", None)
    username = request.user.username
    key = _gen_filename(username, file_name)
    policy = {
        "mimeLimit": "image/*",
    }
    token = auth.upload_token(bucket_name, key, 3600, policy=policy)
    return Response({
        'upload-token': token,
        'key': key,
    }, 200)


@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def upload_user_portrait(request):
    """
    用户上传更新自身的头像
    """
    pass
