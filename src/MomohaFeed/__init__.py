from MomohaFeed.models import Feed, Item, Subscription, ItemRead
import feedparser
from django.db.models import Max
from datetime import datetime
import time
from django.utils.timezone import utc
import calendar
import HTMLParser
from MomohaFeed import feedpoll

       
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

def subscription_list_content(db_subscription,show_readdone=True,show_nonstar=True):
    
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
                        ( MomohaFeed_item.last_poll >= %s )
                    GROUP BY
                        MomohaFeed_item.id
                ) AS I
            WHERE
                ( %s OR ( NOT I.readdone ) ) AND
                ( %s OR ( I.star ) )
            ORDER BY
                I.published DESC ,
                I.id ASC
        ''',
        [
            db_subscription.id,
            db_subscription.id,
            db_subscription.feed.id,
            db_subscription.start,
            show_readdone,
            show_nonstar,
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
    
    db_feed_list = Feed.objects.filter(last_poll__lte = last_poll_max).order_by('last_poll')
    
    for db_feed in db_feed_list:
        feedpoll.poll_feed(db_feed.url, now)
    

def now64():
    
    ret = time.time()
    ret *= 1000
    ret = int(ret)
    return ret
