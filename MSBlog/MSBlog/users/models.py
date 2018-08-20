import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # # 头像
    portrait_url = models.URLField(default=getattr(settings, "DEFAULT_PORTRAIT"))

    def validate_portrait_url(self, url: str) -> bool:
        pass

    def __str__(self):
        return self.username

    # class Meta:
    #     exclude = ('first_name', 'last_name', )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
