from MomohaFeed.models import Feed, Item
import feedparser
from django.db.models import Max
from datetime import datetime
import time
from django.utils.timezone import utc
import calendar

def poll(db_feed):
    now = datetime.now()
    
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
        
        entry_published = entry.published_parsed
        entry_published = datetime.fromtimestamp(calendar.timegm(entry_published),utc)
        
        entry_updated = entry.updated_parsed
        entry_updated = datetime.fromtimestamp(calendar.timegm(entry_updated),utc)
        
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
