import time
from MomohaFeed.models import Subscription
class VmSubscription(object):

    def __init__(self,db_subscription):
        
        self.id = db_subscription.id
        self.link = db_subscription.feed.link
        self.enable = db_subscription.enable
        if hasattr(db_subscription, 'unread_count'):
            self.unread_count = db_subscription.unread_count

        if db_subscription.title != None :
            self.title = db_subscription.title
        else:
            self.title = db_subscription.feed.title


class VmSubscriptionDetail(VmSubscription):

    def __init__(self,db_subscription):
        
        VmSubscription.__init__(self,db_subscription)
        
        self.user = db_subscription.user.id
        self.feed_id = db_subscription.feed.id
        self.url = db_subscription.feed.url
        self.last_poll = db_subscription.feed.last_poll
        self.last_detail_update = db_subscription.feed.last_detail_update
        self.subscription_title = db_subscription.title
        self.feed_title = db_subscription.feed.title

        self.last_poll_txt = time64_to_txt(self.last_poll)
        self.last_detail_update_txt = time64_to_txt(self.last_detail_update)


class VmItem(object):
    
    def __init__(self,db_item):
        
        self.id = db_item.id
        self.title = db_item.title
        self.published = db_item.published
        self.link = db_item.link
        if hasattr(db_item, 'star'):
            self.star = db_item.star
        else:
            self.star = None
        if hasattr(db_item, 'readdone'):
            self.readdone = db_item.readdone
        else:
            self.readdone = None

        self.published_txt = time64_to_txt(self.published)


class VmItemDetail(VmItem):
    
    def __init__(self,db_subscription,db_item):
        
        VmItem.__init__(self,db_item)
        
        self.feed_id = db_item.feed.id
        if type(db_subscription) == Subscription:
            self.subscription_id = db_subscription.id
        else:
            self.subscription_id = db_subscription
        self.last_poll = db_item.last_poll
        self.updated = db_item.updated
        self.content = db_item.content
        self.last_detail_update = db_item.last_detail_update

        self.last_poll_txt = time64_to_txt(self.last_poll)
        self.updated_txt = time64_to_txt(self.updated)
        self.last_detail_update_txt = time64_to_txt(self.last_detail_update)


def time64_to_txt(time64):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(time64/1000))


class VmSubscriptionTag(object):
    
    def __init__(self, db_subscriptiontag):
        self.id = db_subscriptiontag.id
        self.title = db_subscriptiontag.title
        self.enable = db_subscriptiontag.enable


class VmSubscriptionTagSubscriptionRelation(object):
    
    def __init__(self, db_subscriptiontagsubscriptionrelation):
        self.subscriptiontag_id = db_subscriptiontagsubscriptionrelation.subscription_tag.id
        self.subscription_id = db_subscriptiontagsubscriptionrelation.subscription.id


class VmSubscriptionTagDetail(object):

    def __init__(self,db_subscriptiontag):
        
        self.id = db_subscriptiontag.id
        self.enable = db_subscriptiontag.enable
        self.title = db_subscriptiontag.title
        self.user = db_subscriptiontag.user.id
