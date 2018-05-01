from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    picture = models.ImageField(upload_to='profile_pictures', blank=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Follow(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friends', on_delete=models.CASCADE)
    target  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')
    # @property
    # def activity_notify(self):
        # return [feed_manager.get_notification_feed(self.target_user.id)]

def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)

def follow_feed(sender, instance, created, **kwargs):
    if created:
        feed_manager.follow_user(instance.user_id, instance.target_id)


signals.post_delete.connect(unfollow_feed, sender=Follow, dispatch_uid='8f71057f-8cca')
signals.post_save.connect(follow_feed, sender=Follow, dispatch_uid='3af05901-3f18')
