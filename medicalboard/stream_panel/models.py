from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from stream_django.activity import Activity
import uuid


# Create your models here.
class Panel(models.Model, Activity):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def activity_actor_attr(self):
        return self
