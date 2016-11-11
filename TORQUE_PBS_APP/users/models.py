from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import profile_image_path


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)

    def __unicode__(self):
        return self.username

    def __getitem__(self, item):
        return self.username

    class Meta(object):
        unique_together = ('email',)