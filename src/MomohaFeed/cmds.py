from django.core.exceptions import PermissionDenied
from MomohaFeed.models import Subscription, Item, ItemRead
from MomohaFeed.viewmodels import VmSubscription, VmItem, VmItemDetail
import MomohaFeed
from MomohaFeed import now64


def u403(f):
    def ff(request,*args,**kwargs):
        if request.user == None:
            raise PermissionDenied
        return f(request,*args,**kwargs)
    return ff


@u403
def cmd_list_subscription(request):
    
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
def cmd_add_subscription(request,url):

    db_feed,db_subscription = MomohaFeed.subscription_add(request.user,url)
    MomohaFeed.feed_poll(db_feed)
    return {
        'success': True,
        'subscription' : VmSubscription(db_subscription).__dict__
    }


@u403
def cmd_subscription_set_enable(request,subscription_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_subscription.enable = value
    db_subscription.save()
    
    return { 'success' : True }


@u403
def cmd_subscription_list_item(request,subscription_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription)
    
    item_list = []
    for db_item in db_item_list:
        item_list.append(VmItem(db_item).__dict__)

    return { 'item_list' : item_list }


@u403
def cmd_subscription_list_item_detail(request,subscription_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription)
    
    item_detail_list = []
    for db_item in db_item_list:
        item_detail_list.append(VmItemDetail(db_item).__dict__)

    return { 'item_detail_list' : item_detail_list }


@u403
def cmd_subscription_item_detail(request,subscription_id,item_id):
    
    # db_item = Item.objects.get(id=item_id)
    db_item = MomohaFeed.subscription_item_detail(subscription_id, item_id)
    
    return { 'item_detail': VmItemDetail(db_item).__dict__ }


@u403
def cmd_subscription_item_set_readdone(request,subscription_id,item_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_item = Item.objects.get(id=item_id)

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
def cmd_subscription_poll(request,subscription_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    MomohaFeed.feed_poll(db_subscription.feed)

    return {
        'success': True,
    }