from MomohaFeed.models import Feed, Poll, FeedDetail
import feedparser
from django.db.models import Max

def poll(feed_id):
    db_feed = Feed.objects.get(id=feed_id)
    url = db_feed.url
    feed = feedparser.parse(url)
    
    db_poll = Poll.objects.create(
        feed = db_feed
    )
    
    feed_title = feed.feed.title
    feed_link = feed.feed.link
    
    effective_db_feeddetail = None
    try:
        effective_db_feeddetail = FeedDetail.objects.filter(poll_start__feed__exact=db_feed).latest('poll_start__time')
    except FeedDetail.DoesNotExist:
        effective_db_feeddetail = None
    
    if effective_db_feeddetail == None or feed_title != effective_db_feeddetail.title or feed_link != effective_db_feeddetail.link :
        FeedDetail.objects.create(
            poll_start = db_poll,
            title = feed_title,
            link = feed_link
        )
    
    pass
