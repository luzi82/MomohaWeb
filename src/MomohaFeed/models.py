from django.db import models
from django.contrib.auth import models as auth_models

URL_LENGTH = 1024
TITLE_LENGTH = 1024
KEY_LENGTH = 256
DESCRIPTION_LENGTH = 65536

class Feed(models.Model):

    url = models.CharField(max_length=URL_LENGTH,db_index=True)


class Item(models.Model):
    
    feed = models.ForeignKey(Feed,db_index=True)
    key = models.CharField(max_length=KEY_LENGTH,db_index=True)


class Content(models.Model):
    
    item = models.ForeignKey(Item,db_index=True)
    title = models.CharField(max_length=TITLE_LENGTH)
    time = models.DateTimeField(db_index=True)
    description = models.CharField(max_length=DESCRIPTION_LENGTH)


class Poll(models.Model):
    
    feed = models.ForeignKey(Feed,db_index=True)
    time = models.DateTimeField(db_index=True)
    
    
class PollContent(models.Model):

    poll_start = models.ForeignKey(Poll,db_index=True,related_name='pollcontent_poll_start')
    poll_end = models.ForeignKey(Poll,db_index=True,related_name='pollcontent_poll_end')
    content = models.ForeignKey(Content,db_index=True)


class FeedDetail(models.Model):

    poll_start = models.ForeignKey(Poll,db_index=True)
    title = models.CharField(max_length=TITLE_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_LENGTH)


class Subscription(models.Model):

    user = models.ForeignKey(auth_models.User,db_index=True)
    poll = models.ForeignKey(Poll,db_index=True)
    enable = models.BooleanField(db_index=True)


SUBSCRIPTIONCONTENT_STATE_UNREAD = 0
SUBSCRIPTIONCONTENT_STATE_READ = 1

class SubscriptionContent(models.Model):
    
    subscription = models.ForeignKey(Subscription,db_index=True)
    content = models.ForeignKey(Content,db_index=True)
    state = models.IntegerField(db_index=True)
