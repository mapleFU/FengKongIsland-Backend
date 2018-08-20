import uuid

from django.db import models

from ..users.models import User


# Create your models here.
class TimeStampModel(models.Model):
    # 创建的时间
    created_time = models.DateField(auto_now_add=True)
    # 保存的时间
    saved_time = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    # uuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 表示标志了这个TAG的文章
    posts = models.ManyToManyField('Post')


class Post(TimeStampModel):
    # uid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 标题, 可以考虑添加索引
    title = models.CharField(max_length=100)
    # 文章的内容，属于文本内容
    content = models.TextField(null=False)
    # 作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 阅读量
    reading = models.IntegerField(default=0)


class Comment(models.Model):
    """
    文章的评论
    """
    pass


class Directory(models.Model):
    """
    文章所在的目录
    """
    pass

