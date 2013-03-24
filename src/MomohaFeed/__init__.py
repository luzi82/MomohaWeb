from MomohaFeed.models import Feed
import feedparser
from django.db.models import Max
from datetime import datetime

def poll(feed_id):
    now = datetime.now()
    
    db_feed = Feed.objects.get(id=feed_id)
    url = db_feed.url
    parse_result = feedparser.parse(url)
    
    db_feed.last_update = now
    
    feed_title = parse_result.feed.title
    feed_link = parse_result.feed.link
    if db_feed.title != feed_title or db_feed.link != feed_link:
        db_feed.title = feed_title
        db_feed.link = feed_link
        db_feed.last_detail_update = now
        
    db_feed.save()
    
    
    
    pass
