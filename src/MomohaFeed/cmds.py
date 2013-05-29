from django.core.exceptions import PermissionDenied, ValidationError
from MomohaFeed.models import Subscription, Item, ItemRead, ItemStar,\
    SubscriptionTag, SubscriptionTagSubscriptionRelation
from MomohaFeed.viewmodels import VmSubscription, VmItem, VmItemDetail,\
    VmSubscriptionDetail, VmSubscriptionTag,\
    VmSubscriptionTagSubscriptionRelation, VmSubscriptionTagDetail
import MomohaFeed
from MomohaFeed import now64, enum
import inspect
import urlparse
import xml.dom.minidom
import simplejson
from xml.dom import Node
from lxml import etree
import threading
from django.conf import settings
import sys


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
        
    db_subscriptiontag_list = SubscriptionTag.objects.filter(
        user = request.user,
        enable = True
    )
    subscriptiontag_list = []
    for db_subscriptiontag in db_subscriptiontag_list:
        subscriptiontag_list.append(VmSubscriptionTag(db_subscriptiontag).__dict__)
    
    db_subscriptiontagsubscriptionrelation_list = SubscriptionTagSubscriptionRelation.objects.filter(
        subscription_tag__user = request.user ,
        subscription_tag__enable = True
    )
    subscriptiontagsubscriptionrelation_list = []
    for db_subscriptiontagsubscriptionrelation in db_subscriptiontagsubscriptionrelation_list:
        subscriptiontagsubscriptionrelation_list.append(VmSubscriptionTagSubscriptionRelation(db_subscriptiontagsubscriptionrelation).__dict__)
    
    return {
        'subscription_list': subscription_list,
        'subscriptiontag_list': subscriptiontag_list,
        'subscriptiontagsubscriptionrelation_list': subscriptiontagsubscriptionrelation_list,
    }


@u403
@cmd
def add_subscription(request,url):
    
    ret = MomohaFeed._add_subscription(request.user, url)
#    return {
#        'success': ret['success'],
#        'subscription' : VmSubscription(ret['db_subscription']).__dict__
#    }
    rett = {
        'success': ret['success'],
    }
    if 'db_subscription' in ret:
        rett['subscription'] = VmSubscription(ret['db_subscription']).__dict__
    if 'fail_reason' in ret:
        rett['fail_reason'] = ret['fail_reason']
    return rett
    
    
#    now = MomohaFeed.now64()
#
#    urlparse_result = urlparse.urlparse(url)
#    urlparse_good = True
#    urlparse_good = urlparse_good and (urlparse_result.scheme in ['http','https'])
#    urlparse_good = urlparse_good and (urlparse_result.netloc != "")
#    
#    if not urlparse_good:
#        return {
#            'success': False,
#            'fail_reason': enum.FailReason.BAD_URL,
#        }
#        
#    db_feed = None
#    
#    if db_feed == None:
#        db_feed = MomohaFeed.feedpoll.poll_feed(url, now)
#    
#    if db_feed == None:
#        url2 = MomohaFeed.feedpoll.poll_html(url)
#        if url2 != None:
#            db_feed = MomohaFeed.feedpoll.poll_feed(url2, now)
#
#    if db_feed == None:
#        return {
#            'success': False,
#            'fail_reason': enum.FailReason.BAD_FEED_SOURCE,
#        }
#        
#    db_subscription = MomohaFeed.add_subscription(request.user, db_feed)
#
#    return {
#        'success': True,
#        'subscription' : VmSubscription(db_subscription).__dict__
#    }


@u403
@cmd
def subscription_set_enable(request,subscription_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_subscription.enable = value
    db_subscription.save()
    
    return { 'success' : True }


@u403
@cmd
def subscription_set_title(request,subscription_id,value):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    db_subscription.title = value
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
def subscription_list_item_detail(request,subscription_id,show_readdone,range_published=None,range_id=None,item_count=None):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(
        db_subscription,
        show_readdone=show_readdone,
        range_published=range_published,
        range_id=range_id,
        item_count=item_count
    )
    
    item_detail_list = []
    for db_item in db_item_list:
        item_detail_list.append(VmItemDetail(db_subscription,db_item).__dict__)

    return { 'item_detail_list' : item_detail_list, 'now' : MomohaFeed.now64() }


@u403
@cmd
def subscription_item_detail(request,subscription_id,item_id):

    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied
    
    # db_item = Item.objects.get(id=item_id)
    db_item = MomohaFeed.subscription_item_detail(subscription_id, item_id)
    
    return { 'item_detail': VmItemDetail(db_subscription,db_item).__dict__ }


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
def subscription_all_readdone(request,subscription_id,range_first_poll=None):
    
    db_subscription = Subscription.objects.get(id=subscription_id)
    if(db_subscription.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscription_list_content(db_subscription,show_readdone=False,range_first_poll=range_first_poll)
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


@u403
@cmd
def add_subscriptiontag(request, title):
    
    db_subscriptiontag = SubscriptionTag.objects.create(
        user = request.user,
        title = title,
    )
    return {
        'success': True,
        'subscriptiontag': VmSubscriptionTag(db_subscriptiontag).__dict__
    }

@u403
@cmd
def subscriptiontag_set_title(request, subscriptiontag_id, title):
    
    db_subscriptiontag = SubscriptionTag.objects.get(id=subscriptiontag_id)
    if(db_subscriptiontag.user != request.user):
        raise PermissionDenied

    db_subscriptiontag.title = title
    db_subscriptiontag.save()
    
    return {'success': True}


@u403
@cmd
def subscriptiontag_set_enable(request, subscriptiontag_id, enable):
    db_subscriptiontag = SubscriptionTag.objects.get(id=subscriptiontag_id)
    if(db_subscriptiontag.user != request.user):
        raise PermissionDenied

    db_subscriptiontag.enable = enable
    db_subscriptiontag.save()
    
    return {'success': True}


@u403
@cmd
def subscriptiontag_detail(request,subscriptiontag_id):

    db_subscriptiontag = SubscriptionTag.objects.get(id=subscriptiontag_id)
    if(db_subscriptiontag.user != request.user):
        raise PermissionDenied

    return { 'subscriptiontag_detail' : VmSubscriptionTagDetail(db_subscriptiontag).__dict__ }


@u403
@cmd
def subscriptiontag_list_item_detail(request,subscriptiontag_id,show_readdone,range_published=None,range_id=None,item_count=None):

    db_subscriptiontag = SubscriptionTag.objects.get(id=subscriptiontag_id)
    if(db_subscriptiontag.user != request.user):
        raise PermissionDenied

    db_item_list = MomohaFeed.subscriptiontag_list_content(
        db_subscriptiontag,
        show_readdone=show_readdone,
        range_published=range_published,
        range_id=range_id,
        item_count=item_count
    )
    
    item_detail_list = []
    for db_item in db_item_list:
        item_detail_list.append(VmItemDetail(db_item.subscription_id,db_item).__dict__)

    return { 'item_detail_list' : item_detail_list }


@u403
@cmd
def subscriptiontagsubscription_set(request, set_list):
    
    for set_item in set_list:

        db_subscriptiontag = SubscriptionTag.objects.get(id=set_item['subscriptiontag_id'])
        if(db_subscriptiontag.user != request.user):
            raise PermissionDenied
    
        db_subscription = Subscription.objects.get(id=set_item['subscription_id'])
        if(db_subscription.user != request.user):
            raise PermissionDenied
        
    for set_item in set_list:

        db_subscriptiontag = SubscriptionTag.objects.get(id=set_item['subscriptiontag_id'])
        db_subscription = Subscription.objects.get(id=set_item['subscription_id'])
        
        if set_item['enable']:
            SubscriptionTagSubscriptionRelation.objects.get_or_create(
                subscription_tag = db_subscriptiontag,
                subscription = db_subscription
            )
        else:
            SubscriptionTagSubscriptionRelation.objects.filter(
                subscription_tag = db_subscriptiontag,
                subscription = db_subscription
            ).delete()

    return {'success': True}


@u403
@cmd
def import_opml(request, postfile):
    if(postfile.size>1024*512):
        return {'success':False, 'fail_reason':enum.FailReason.BAD_FILE_SIZE}
    
#    fileraw = postfile.read()
#    dom = xml.dom.minidom.parseString(fileraw)
    tree = etree.parse(postfile)
#    import_result_list = []

    runtime_dict = {
        "target_dict_list": [],
        "offset": 0,
        "cv": threading.Condition(),
        "rssoutline_to_dbid": {},
    }
    
    for outline in tree.findall(".//outline[@type][@xmlUrl][@text]"):
        if outline.get('type') != 'rss':
            continue
        
        xmlUrl = outline.get('xmlUrl')
        text = outline.get('text')

        target_dict = {
            'url': xmlUrl,
            'title': text,
            'success': False,
            'path': tree.getpath(outline)
        }
#        print simplejson.dumps(target_dict)
        runtime_dict['target_dict_list'].append(target_dict)
    
    runtime_dict['target_len'] = len(runtime_dict['target_dict_list'])

    def thread_unit(runtime_dict):
        print "thread start"
        while True:
            try:
                runtime_dict['cv'].acquire()
                print "acquire"
                if runtime_dict['offset'] >= runtime_dict['target_len']:
                    runtime_dict['cv'].release()
                    return
                target_dict = runtime_dict['target_dict_list'][runtime_dict['offset']]
                runtime_dict['offset'] += 1
                print "release"
                runtime_dict['cv'].release()
                
                ret = MomohaFeed._add_subscription(request.user, target_dict['url'])
                if not ret['success']:
                    target_dict['fail_reason'] = ret['fail_reason']
                    continue
                target_dict['success'] = True
                target_dict['subscription_id'] = ret['db_subscription'].id
                if(
                    (
                        (ret['db_subscription'].feed.title != target_dict['title']) and
                        (ret['db_subscription'].title == None)
                    ) or
                    (ret['db_subscription'].title != target_dict['title'])
                ):
                    ret['db_subscription'].title = target_dict['title']
                    ret['db_subscription'].save()
                runtime_dict["rssoutline_to_dbid"][target_dict['path']] = ret['db_subscription'].id
            except Exception as e:
                print e
        print "thread end"

    if 'test' in sys.argv:
        # django+test+thread+db problem work-around
        thread_unit(runtime_dict)
    else:
        thread_list = []            
        for _ in range(settings.OPML_IMPORT_THREAD_COUNT):
            t = threading.Thread(target=thread_unit,args=(runtime_dict,))
            thread_list.append(t)
            t.start()
        
        for t in thread_list:
            t.join()

    for outline in tree.xpath('/opml/body/outline[@text]'):
        if outline.get('type')!=None:
            continue
        if outline.get('xmlUrl')!=None:
            continue
        db_subscriptiontag, _ = SubscriptionTag.objects.get_or_create(
            user = request.user,
            title = outline.get('text'),
        )
        for outline2 in outline.findall('.//outline[@type][@xmlUrl][@text]'):
            if not tree.getpath(outline2) in runtime_dict["rssoutline_to_dbid"]:
                continue;
            db_subscription_id = runtime_dict["rssoutline_to_dbid"][tree.getpath(outline2)]
            db_subscription = Subscription.objects.get(id=db_subscription_id)
            SubscriptionTagSubscriptionRelation.objects.get_or_create(
                subscription_tag = db_subscriptiontag,
                subscription = db_subscription,
            )
                

    return {
        'success': True,
    }
