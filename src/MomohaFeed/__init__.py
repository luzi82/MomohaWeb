from MomohaFeed.models import Feed, Item, Subscription, ItemRead
import feedparser
from django.db.models import Max
from datetime import datetime
import time
from django.utils.timezone import utc
import calendar
import HTMLParser

def feed_poll(db_feed):
    now = now64()
    
    htmlparser = HTMLParser.HTMLParser()
    
    url = db_feed.url
    parse_result = feedparser.parse(url)
    
    db_feed.last_poll = now
    
    feed_title = parse_result.feed.title
    feed_link = parse_result.feed.link
    if db_feed.title != feed_title or db_feed.link != feed_link:
        db_feed.title = feed_title
        db_feed.link = feed_link
        db_feed.last_detail_update = now
        
    db_feed.save()
    
    for entry in parse_result.entries:
        
        db_item,item_create = Item.objects.get_or_create(
             feed = db_feed,
             key = entry.id
        )

        db_item.last_poll = now

        entry_content = None
        if hasattr(entry,'content') and len(entry.content) >= 1:
            entry_content = entry.content[0].value
        elif hasattr(entry,'summary'):
            entry_content = entry.summary
            
        if entry_content != None:
            entry_content = htmlparser.unescape(entry_content)
        
        entry_published = None
        if hasattr(entry,'published_parsed'):
            entry_published = entry.published_parsed
            entry_published = int(calendar.timegm(entry_published)*1000)
        
        entry_updated = None
        if hasattr(entry,'updated_parsed'):
            entry_updated = entry.updated_parsed
            entry_updated = int(calendar.timegm(entry_updated)*1000)
        
        if entry_published == None:
            entry_published = entry_updated
        if entry_updated == None:
            entry_updated = entry_published
        
        if (
            item_create or
            db_item.title != entry.title or
            db_item.published != entry_published or
            db_item.updated != entry_updated or
            db_item.link != entry.link or
            db_item.content != entry_content
        ):
            db_item.title = entry.title
            db_item.published = entry_published
            db_item.updated = entry_updated
            db_item.link = entry.link
            db_item.content = entry_content
            db_item.last_detail_update = now
        
        db_item.save()

def subscription_add(db_user,url):
    
    db_feed,_ = Feed.objects.get_or_create(
        url = url
    )
    db_subscription,_ = Subscription.objects.get_or_create(
        user = db_user,
        feed = db_feed,
        enable = True,
        defaults = {'start': now64()}
    )
    
    return db_feed,db_subscription

def subscription_list_content(db_subscription):

    db_item_list = Item.objects.raw(
        '''
            SELECT
                MomohaFeed_item.*,
                (Count(MomohaFeed_itemread.enable)>0) readdone
            FROM
                MomohaFeed_item
                LEFT JOIN MomohaFeed_itemread
                    ON (
                        MomohaFeed_itemread.item_id = MomohaFeed_item.id AND
                        MomohaFeed_itemread.subscription_id = %s AND
                        MomohaFeed_itemread.enable
                    )
            WHERE
                MomohaFeed_item.feed_id = %s
            GROUP BY
                MomohaFeed_item.id
            ORDER BY
                MomohaFeed_item.published DESC
        ''',
        [
            db_subscription.id, db_subscription.feed.id
        ]
    )

    return db_item_list;

def subscription_item_mark_read(db_subscription,db_item):

    ItemRead.objects.get_or_create(
        subscription = db_subscription,
        item = db_item,
        enable = True,
        defaults = {'time': now64()}
    )

def now64():
    
    ret = time.time()
    ret *= 1000
    ret = int(ret)
    return ret
