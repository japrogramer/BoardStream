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
    text = models.CharField(max_length=250)

    @property
    def activity_actor_attr(self):
        return self

    @property
    def activity_notify(self):
        targets = [feed_manager.get_news_feeds(self.author_id)['timeline']]
        # TODO: maybe add this
        # for hashtag in self.parse_hashtags():
            # targets.append(feed_manager.get_feed('user', 'hash_%s' % hashtag))
        # for user in self.parse_mentions():
            # targets.append(feed_manager.get_news_feeds(user.id)['timeline'])
        return targets


class Comments(models.Model, Activity):
    panel =  models.ForeignKey('stream_panel.Panel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)

    @property
    def activity_actor_attr(self):
        return self

    @property
    def activity_notify(self):
        targets = [feed_manager.get_news_feeds(self.author_id)['timeline']]
        # TODO: maybe add this
        # for hashtag in self.parse_hashtags():
            # targets.append(feed_manager.get_feed('user', 'hash_%s' % hashtag))
        # for user in self.parse_mentions():
            # targets.append(feed_manager.get_news_feeds(user.id)['timeline'])
        return targets
