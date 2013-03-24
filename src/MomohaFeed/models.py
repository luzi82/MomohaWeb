from django.db import models
from django.contrib.auth import models as auth_models

URL_LENGTH = 1024
TITLE_LENGTH = 1024
KEY_LENGTH = 256
CONTENT_LENGTH = 65536

class Feed(models.Model):

    url = models.CharField(max_length=URL_LENGTH,db_index=True)
    last_update = models.DateTimeField(db_index=True,null=True)

    title = models.CharField(max_length=TITLE_LENGTH,null=True)
    link = models.CharField(max_length=URL_LENGTH,null=True)
    last_detail_update = models.DateTimeField(null=True)

class Item(models.Model):
    
    feed = models.ForeignKey(Feed,db_index=True)
    key = models.CharField(max_length=KEY_LENGTH,db_index=True)
    last_exist = models.DateTimeField(db_index=True,null=True)
    
    title = models.CharField(max_length=TITLE_LENGTH,null=True)
    time = models.DateTimeField(null=True)
    link = models.CharField(max_length=URL_LENGTH,null=True)
    content = models.CharField(max_length=CONTENT_LENGTH,null=True)
    last_detail_update = models.DateTimeField(null=True)


class Subscription(models.Model):

    user = models.ForeignKey(auth_models.User,db_index=True)
    feed = models.ForeignKey(Feed,db_index=True)
    start = models.DateTimeField(auto_now_add=True)
    enable = models.BooleanField(db_index=True)


class ItemRead(models.Model):
    
    subscription = models.ForeignKey(Subscription,db_index=True)
    item = models.ForeignKey(Item,db_index=True)
    time = models.DateTimeField(db_index=True,auto_now_add=True)
