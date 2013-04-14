import time
class VmSubscription(object):

    def __init__(self,db_subscription):
        
        self.id = db_subscription.id
        self.title = db_subscription.feed.title
        self.link = db_subscription.feed.link
        self.enable = db_subscription.enable


class VmSubscriptionDetail(VmSubscription):

    def __init__(self,db_subscription):
        
        VmSubscription.__init__(self,db_subscription)
        
        self.user = db_subscription.user.id
        self.feed_id = db_subscription.feed.id
        self.url = db_subscription.feed.url
        self.last_poll = time64_to_str(db_subscription.feed.last_poll)
        self.last_detail_update = time64_to_str(db_subscription.feed.last_detail_update)


class VmItem(object):
    
    def __init__(self,db_item):
        
        self.id = db_item.id
        self.title = db_item.title
        self.published = time64_to_str(db_item.published)
        self.link = db_item.link
        if hasattr(db_item, 'readdone'):
            self.readdone = db_item.readdone
        else:
            self.readdone = None


class VmItemDetail(VmItem):
    
    def __init__(self,db_item):
        
        VmItem.__init__(self,db_item)
        
        self.feed_id = db_item.feed.id
        self.last_poll = time64_to_str(db_item.last_poll)
        self.updated = time64_to_str(db_item.updated)
        self.content = db_item.content
        self.last_detail_update = time64_to_str(db_item.last_detail_update)


def time64_to_str(time64):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(time64/1000))
