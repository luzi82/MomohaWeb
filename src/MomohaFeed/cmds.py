from django.core.exceptions import PermissionDenied, ValidationError
from MomohaFeed.models import Subscription, Item, ItemRead, ItemStar
from MomohaFeed.viewmodels import VmSubscription, VmItem, VmItemDetail,\
    VmSubscriptionDetail
import MomohaFeed
from MomohaFeed import now64, enum
import inspect
import urlparse


cmd_list = []
cmd_dict = {}

def cmd(f):
    argv = inspect.getargspec(f)[0]
    argv = argv[1:]
    cmd_list.append({
         'name': f.func_name,
         'argv': argv,
    })
    cmd_dict[f.func_name]=f
    return f


def u403(f):
    def ff(request,*args,**kwargs):
        if request.user == None:
            raise PermissionDenied
        return f(request,*args,**kwargs)
    return ff


@u403
@cmd
def list_subscription(request):
    
    db_subscription_list = Subscription.objects.filter(
        user__exact = request.user,
        enable__exact = True
    ).select_related("feed")
    
    subscription_list = []
    for db_subscription in db_subscription_list:
        subscription_list.append(VmSubscription(db_subscription).__dict__)
    
    return {
        'subscription_list' : subscription_list
    }


@u403
@cmd
def add_subscription(request,url):
    
    now = MomohaFeed.now64()

    urlparse_result = urlparse.urlparse(url)
    urlparse_good = True
    urlparse_good = urlparse_good and (urlparse_result.scheme in ['http','https'])
    urlparse_good = urlparse_good and (urlparse_result.netloc != "")
    
    if not urlparse_good:
        return {
            'success': False,
            'fail_reason': enum.FailReason.BAD_URL,
        }
        
    db_feed = None
    
    if db_feed == None:
        db_feed = MomohaFeed.feedpoll.poll_feed(url, now)
    
    if db_feed == None:
        url2 = MomohaFeed.feedpoll.poll_html(url)
        if url2 != None:
            db_feed = MomohaFeed.feedpoll.poll_feed(url2, now)

    if db_feed == None:
        return {
            'success': False,
            'fail_reason': enum.FailReason.BAD_FEED_SOURCE,
        }
        
    db_subscription = MomohaFeed.add_subscription(request.user, db_feed)

    return {
        'success': True,
        'subscription' : VmSubscription(db_subscription).__dict__
    }


@u403
@cmd
def subscription_set_enable(request,subscription_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_subscription.enable = value
    db_subscription.save()
    
    return { 'success' : True }


#@u403
#@cmd
#def subscription_list_item(request,subscription_id,show_readdone):
#
#    db_subscription = Subscription.objects.get(id=subscription_id)
#    if(db_subscription.user != request.user):
#        raise PermissionDenied
#
#    db_item_list = MomohaFeed.subscription_list_content(db_subscription,show_readdone=show_readdone)
#    
#    item_list = []
#    for db_item in db_item_list:
#        item_list.append(VmItem(db_item).__dict__)
#
#    return { 'item_list' : item_list }


@u403
@cmd
def subscription_list_item_detail(request,subscription_id,show_readdone):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription,show_readdone=show_readdone)
    
    item_detail_list = []
    for db_item in db_item_list:
        item_detail_list.append(VmItemDetail(db_item).__dict__)

    return { 'item_detail_list' : item_detail_list }


@u403
@cmd
def subscription_item_detail(request,subscription_id,item_id):
    
    # db_item = Item.objects.get(id=item_id)
    db_item = MomohaFeed.subscription_item_detail(subscription_id, item_id)
    
    return { 'item_detail': VmItemDetail(db_item).__dict__ }


@u403
@cmd
def subscription_item_set_readdone(request,subscription_id,item_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_item = Item.objects.get(id=item_id)
    if(db_item.feed != db_subscription.feed):
        raise ValidationError

    if value:
        ItemRead.objects.get_or_create(
            subscription = db_subscription,
            item = db_item,
            enable = True,
            defaults = {'time': now64()}
        )
    else:
        ItemRead.objects.filter(
            subscription = db_subscription,
            item = db_item
        ).update(enable = False)

    return { 'success' : True }


@u403
@cmd
def subscription_poll(request,subscription_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    MomohaFeed.feedpoll.poll_feed(db_subscription.feed.url, now64())

    return {
        'success': True,
    }


@u403
@cmd
def subscription_all_readdone(request,subscription_id):
    
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription,show_readdone=False)
    now = now64()

    for db_item in db_item_list:
        ItemRead.objects.get_or_create(
            subscription = db_subscription,
            item = db_item,
            enable = True,
            defaults = {'time': now}
        )

    return { 'success' : True }


@u403
@cmd
def subscription_detail(request,subscription_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    return { 'subscription_detail' : VmSubscriptionDetail(db_subscription).__dict__ }


@u403
@cmd
def subscription_item_set_star(request,subscription_id,item_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item = Item.objects.get(id=item_id)
    if(db_item.feed != db_subscription.feed):
        raise ValidationError

    if value:
        ItemStar.objects.get_or_create(
            subscription = db_subscription,
            item = db_item,
            enable = True,
            defaults = {'time': now64()}
        )
    else:
        ItemStar.objects.filter(
            subscription = db_subscription,
            item = db_item
        ).update(enable = False)

    return { 'success' : True }
