from django.db import models
from django.contrib.auth import models as auth_models

URL_LENGTH = 1024
TITLE_LENGTH = 128

Subscription_CONTENT_STATE_INVISIBLE = 0
Subscription_CONTENT_STATE_UNREAD = 1
Subscription_CONTENT_STATE_READ = 2

class Feed(models.Model):

    url = models.CharField(max_length=URL_LENGTH,db_index=True)
    title = models.CharField(max_length=TITLE_LENGTH)


class Subscription(models.Model):

    user = models.ForeignKey(auth_models.User,db_index=True)
    feed = models.ForeignKey(Feed,db_index=True)


class FeedContent(models.Model):
    
    feed = models.ForeignKey(Feed,db_index=True)
    title = models.CharField(max_length=TITLE_LENGTH)


class SubscriptionContent(models.Model):
    
    content = models.ForeignKey(FeedContent,db_index=True)
    Subscription = models.ForeignKey(Subscription,db_index=True)
    state = models.IntegerField(db_index=True)
