import uuid
import datetime

from django.db import models

from ..users.models import User


# Create your models here.
class TimeStampModel(models.Model):
    # 创建的时间
    created_time = models.DateTimeField(default=datetime.datetime.now)
    # 保存的时间
    saved_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    # uuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 表示标志了这个TAG的文章
    posts = models.ManyToManyField('Post', related_name='tags')
    tag_name = models.CharField(max_length=20, db_index=True, unique=True)
    #count
    related_posts = models.IntegerField(default=0)


class Post(TimeStampModel):
    # uid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 标题, 可以考虑添加索引
    title = models.CharField(max_length=100)
    # 文章的内容，属于文本内容, 文本内容是 markdown
    content = models.TextField(null=False)
    # 作者
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # 阅读量
    reading = models.IntegerField(default=0)
    # 目录
    directory = models.ForeignKey('Directory', related_name='posts', on_delete=models.SET_NULL, null=True)
    # 标签(已有)

    # abstract, 文章的摘要
    abstract = models.CharField(max_length=200, null=True, editable=True)


class Comment(models.Model):
    """
    文章的评论
    """
    pass


class Proverb(models.Model):
    """
    获得的谏言
    只有一句，后台随便添加随便来，关系都没有
    """
    post_by = models.CharField(max_length=30)
    content = models.CharField(max_length=150)


class Directory(models.Model):
    """
    文章所在的目录
    """
    # uid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 名字
    name = models.CharField(max_length=20, db_index=True, null=False)
    # 父目录
    father_directory = models.ForeignKey('self', related_name='child_directories',
                                         null=True, on_delete=models.SET_NULL)
