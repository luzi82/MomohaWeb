from MomohaFeed.models import Feed, Item, Subscription, ItemRead
import feedparser
from django.db.models import Max
from datetime import datetime
import time
from django.utils.timezone import utc
import calendar
import HTMLParser
from MomohaFeed import feedpoll, enum
import urlparse

       
def add_feed(url):
    
    db_feed, _ = Feed.objects.get_or_create(
        url = url
    )

    return db_feed


def add_subscription(db_user,db_feed):

    db_subscription,_ = Subscription.objects.get_or_create(
        user = db_user,
        feed = db_feed,
        enable = True,
        defaults = {'start': db_feed.last_poll}
    )
    
    return db_subscription


def _add_subscription(db_user,url):
    
    now = now64()
    
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
        db_feed = feedpoll.poll_feed(url, now)
    
    if db_feed == None:
        url2 = feedpoll.poll_html(url)
        if url2 != None:
            db_feed = feedpoll.poll_feed(url2, now)

    if db_feed == None:
        return {
            'success': False,
            'fail_reason': enum.FailReason.BAD_FEED_SOURCE,
        }
    
    db_subscription = add_subscription(db_user, db_feed)

    return {
        'success': True,
        'db_subscription' : db_subscription
    }


#def subscription_add(db_user,url):
#    
#    db_feed,_ = Feed.objects.get_or_create(
#        url = url
#    )
#    db_subscription,_ = Subscription.objects.get_or_create(
#        user = db_user,
#        feed = db_feed,
#        enable = True,
#        defaults = {'start': now64()}
#    )
#    
#    return db_feed,db_subscription

def subscription_list_content(
    db_subscription,
    show_readdone=True,
    show_nonstar=True,
    range_published=None,
    range_id=None,
    item_count=None,
    range_first_poll=None,
):
    
    db_item_list = Item.objects.raw(
        '''
            SELECT
                I.*,
                I.readdone
            FROM
                (
                    SELECT
                        MomohaFeed_item.* ,
                        (Count(MomohaFeed_itemread.enable)>0) readdone ,
                        (Count(MomohaFeed_itemstar.enable)>0) star
                    FROM
                        "MomohaFeed_item" as MomohaFeed_item
                        LEFT JOIN "MomohaFeed_itemread" as MomohaFeed_itemread
                            ON (
                                MomohaFeed_itemread.item_id = MomohaFeed_item.id AND
                                MomohaFeed_itemread.subscription_id = %s AND
                                MomohaFeed_itemread.enable
                            )
                        LEFT JOIN "MomohaFeed_itemstar" as MomohaFeed_itemstar
                            ON (
                                MomohaFeed_itemstar.item_id = MomohaFeed_item.id AND
                                MomohaFeed_itemstar.subscription_id = %s AND
                                MomohaFeed_itemstar.enable
                            )
                    WHERE
                        ( MomohaFeed_item.feed_id = %s ) AND
                        ( MomohaFeed_item.last_poll >= %s ) AND
                        (
                            %s OR
                            ( MomohaFeed_item.published < %s ) OR
                            (
                                ( MomohaFeed_item.published = %s ) AND
                                ( MomohaFeed_item.id > %s )
                            )
                        ) AND
                        (
                            %s OR
                            ( MomohaFeed_item.first_poll < %s ) OR
                            ( MomohaFeed_item.first_poll IS NULL )
                        )
                    GROUP BY
                        MomohaFeed_item.id
                ) AS I
            WHERE
                ( %s OR ( NOT I.readdone ) ) AND
                ( %s OR ( I.star ) )
            ORDER BY
                I.published DESC ,
                I.id ASC
            LIMIT %s
        ''',
        [
            db_subscription.id, # MomohaFeed_itemread.subscription_id = %s
            db_subscription.id, # MomohaFeed_itemstar.subscription_id = %s
            db_subscription.feed.id, # MomohaFeed_item.feed_id = %s
            db_subscription.start, # MomohaFeed_item.last_poll >= %s
            ( range_published == None ) and ( range_id == None ) , # %s
            range_published if (range_published!=None) else 0 , # ( MomohaFeed_item.published < %s )
            range_published if (range_published!=None) else 0 , # ( MomohaFeed_item.published = %s )
            range_id if (range_id!=None) else 0 , # ( MomohaFeed_item.id > %s )
            ( range_first_poll == None ) , # %s
            range_first_poll if (range_first_poll!=None) else 0 , # ( MomohaFeed_item.first_poll < %s )
            show_readdone, # ( %s OR ( NOT I.readdone )
            show_nonstar, # ( %s OR ( I.star ) )
            item_count if (item_count!=None) else 0x7fffffff # LIMIT %s, issue 109
        ]
    )

    return db_item_list;


def subscription_item_detail(subscription_id, item_id):
    
#    db_item = Item.objects.get(id=item_id)
    db_item_list = Item.objects.raw(
        '''
            SELECT
                MomohaFeed_item.* ,
                (Count(MomohaFeed_itemread.enable)>0) readdone ,
                (Count(MomohaFeed_itemstar.enable)>0) star
            FROM
                "MomohaFeed_item" as MomohaFeed_item
                LEFT JOIN "MomohaFeed_itemread" as MomohaFeed_itemread
                    ON (
                        MomohaFeed_itemread.item_id = MomohaFeed_item.id AND
                        MomohaFeed_itemread.subscription_id = %s AND
                        MomohaFeed_itemread.enable
                    )
                LEFT JOIN "MomohaFeed_itemstar" as MomohaFeed_itemstar
                    ON (
                        MomohaFeed_itemstar.item_id = MomohaFeed_item.id AND
                        MomohaFeed_itemstar.subscription_id = %s AND
                        MomohaFeed_itemstar.enable
                    )
            WHERE
                MomohaFeed_item.id = %s
            ORDER BY
                MomohaFeed_item.published DESC ,
                MomohaFeed_item.id ASC
        ''',
        [
            subscription_id,
            subscription_id,
            item_id
        ]
    )
    
    return db_item_list[0]


def subscription_item_mark_read(db_subscription,db_item):

    ItemRead.objects.get_or_create(
        subscription = db_subscription,
        item = db_item,
        enable = True,
        defaults = {'time': now64()}
    )
    
    
def update_feed_pool(ms):
    
    now = now64()
    last_poll_max = now-ms
    start = now
    
    db_feed_list = Feed.objects.filter(last_poll__lte = last_poll_max).order_by('last_poll')
    
    for db_feed in db_feed_list:
        feedpoll.poll_feed(db_feed.url, now64())
        if now64()-start > 40*1000:
            break


def subscriptiontag_list_content(
    db_subscriptiontag,
    show_readdone=True,
    show_nonstar=True,
    range_published=None,
    range_id=None,
    item_count=None,
):
    
    db_item_list = Item.objects.raw(
        '''
            SELECT
                I.*,
                I.readdone
            FROM
                (
                    SELECT
                        MomohaFeed_item.* ,
                        MomohaFeed_subscription.id subscription_id,
                        (Count(MomohaFeed_itemread.enable)>0) readdone ,
                        (Count(MomohaFeed_itemstar.enable)>0) star
                    FROM
                        "MomohaFeed_subscriptiontagsubscriptionrelation" as MomohaFeed_subscriptiontagsubscriptionrelation
                        JOIN "MomohaFeed_subscription" as MomohaFeed_subscription
                            ON (
                                MomohaFeed_subscription.id = MomohaFeed_subscriptiontagsubscriptionrelation.subscription_id AND
                                MomohaFeed_subscription.enable
                            )
                        JOIN "MomohaFeed_item" as MomohaFeed_item
                            ON (
                                MomohaFeed_item.feed_id = MomohaFeed_subscription.feed_id AND
                                MomohaFeed_item.last_poll >= MomohaFeed_subscription.start
                            )
                        LEFT JOIN "MomohaFeed_itemread" as MomohaFeed_itemread
                            ON (
                                MomohaFeed_itemread.item_id = MomohaFeed_item.id AND
                                MomohaFeed_itemread.subscription_id = MomohaFeed_subscription.id AND
                                MomohaFeed_itemread.enable
                            )
                        LEFT JOIN "MomohaFeed_itemstar" as MomohaFeed_itemstar
                            ON (
                                MomohaFeed_itemstar.item_id = MomohaFeed_item.id AND
                                MomohaFeed_itemstar.subscription_id = MomohaFeed_subscription.id AND
                                MomohaFeed_itemstar.enable
                            )
                    WHERE
                        ( MomohaFeed_subscriptiontagsubscriptionrelation.subscription_tag_id = %s ) AND
                        (
                            %s OR
                            ( MomohaFeed_item.published < %s ) OR
                            (
                                ( MomohaFeed_item.published = %s ) AND
                                ( MomohaFeed_item.id > %s )
                            )
                        )
                    GROUP BY
                        MomohaFeed_item.id ,
                        MomohaFeed_subscription.id
                ) AS I
            WHERE
                ( %s OR ( NOT I.readdone ) ) AND
                ( %s OR ( I.star ) )
            ORDER BY
                I.published DESC ,
                I.id ASC
            LIMIT %s
        ''',
        [
            db_subscriptiontag.id, # ( MomohaFeed_subscriptiontagsubscriptionrelation.subscriptiontag_id = %s )
            ( range_published == None ) and ( range_id == None ) , # %s
            range_published if (range_published!=None) else 0 , # ( MomohaFeed_item.published < %s )
            range_published if (range_published!=None) else 0 , # ( MomohaFeed_item.published == %s )
            range_id if (range_id!=None) else 0 , # ( MomohaFeed_item.id > %s )
            show_readdone, # ( %s OR ( NOT I.readdone )
            show_nonstar, # ( %s OR ( I.star ) )
            item_count if (item_count!=None) else 0x7fffffff # LIMIT %s, issue 109
        ]
    )

    return db_item_list;


def now64():
    
    ret = time.time()
    ret *= 1000
    ret = int(ret)
    return ret
