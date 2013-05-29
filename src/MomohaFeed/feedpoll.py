import HTMLParser
import feedparser
import MomohaFeed
from MomohaFeed.models import Item
import calendar
import urllib2
import lxml.html
import pprint
import traceback


def poll_feed(url, now):
    """if success, return db_feed, otherwise None"""
    print("poll_feed "+url)
    
    htmlparser = HTMLParser.HTMLParser()
    
    parse_result = feedparser.parse(url)
    
    if ( not parse_result.has_key('version') ) or ( parse_result['version'] == '' ):
        print("poll_feed "+url+" fail")
        return None
    
    print("poll_feed "+url+" ok")
    
    db_feed, _ = MomohaFeed.models.Feed.objects.get_or_create(
        url = url,
    )
    
    db_feed.last_poll = now
    
    feed_title = parse_result.feed.title
    feed_link = parse_result.feed.link
    if db_feed.title != feed_title or db_feed.link != feed_link:
        db_feed.title = feed_title
        db_feed.link = feed_link
        db_feed.last_detail_update = now
        
    db_feed.save()
    
    for entry in parse_result.entries:
        
        if hasattr(entry,'id'):
            entry_id = entry.id
        else:
            entry_id = ""
            if hasattr(entry,'link'):
                entry_id += entry.link
            entry_id += "-"
            if hasattr(entry,'title'):
                entry_id += entry.title
            entry_id += "-"
            if hasattr(entry,'published'):
                entry_id += entry.published
        
        db_item,item_create = Item.objects.get_or_create(
             feed = db_feed,
             key = entry_id
        )

        db_item.last_poll = now
        if item_create :
            db_item.first_poll = now

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
            
        entry_title = None
        if hasattr(entry,'title'):
            entry_title = entry.title
        
        entry_link = None
        if hasattr(entry,'link'):
            entry_link = entry.link
        
        if (
            item_create or
            db_item.title != entry_title or
            db_item.published != entry_published or
            db_item.updated != entry_updated or
            db_item.link != entry_link or
            db_item.content != entry_content
        ):
            db_item.title = entry_title
            db_item.published = entry_published
            db_item.updated = entry_updated
            db_item.link = entry_link
            db_item.content = entry_content
            db_item.last_detail_update = now
        
        db_item.save()

    return db_feed


def poll_html(url):
    """return url of feed pointed by html, or None"""
    print("poll_html "+url)

    try:
        content = urllib2.urlopen(url).read()
        tree = lxml.html.fromstring(content)
    
        headV = tree.findall('head')
        for head in headV:
            linkV = head.findall('link')
            for link in linkV:
                if link.get('rel') != 'alternate':
                    continue
                link_type = link.get('type')
                if not ( link_type == 'application/atom+xml' or link_type == 'application/rss+xml' ):
                    continue
                return link.get('href')
    
        return None

    except Exception:
        return None

#def feed_poll(db_feed):
#    
#    try:
#    
#        htmlparser = HTMLParser.HTMLParser()
#        
#        url = db_feed.url
#        parse_result = feedparser.parse(url)
#        
#        now = MomohaFeed.now64()
#        db_feed.last_poll = now
#        
#        feed_title = parse_result.feed.title
#        feed_link = parse_result.feed.link
#        if db_feed.title != feed_title or db_feed.link != feed_link:
#            db_feed.title = feed_title
#            db_feed.link = feed_link
#            db_feed.last_detail_update = now
#            
#        db_feed.save()
#        
#        for entry in parse_result.entries:
#            
#            db_item,item_create = Item.objects.get_or_create(
#                 feed = db_feed,
#                 key = entry.id
#            )
#    
#            db_item.last_poll = now
#    
#            entry_content = None
#            if hasattr(entry,'content') and len(entry.content) >= 1:
#                entry_content = entry.content[0].value
#            elif hasattr(entry,'summary'):
#                entry_content = entry.summary
#                
#            if entry_content != None:
#                entry_content = htmlparser.unescape(entry_content)
#            
#            entry_published = None
#            if hasattr(entry,'published_parsed'):
#                entry_published = entry.published_parsed
#                entry_published = int(calendar.timegm(entry_published)*1000)
#            
#            entry_updated = None
#            if hasattr(entry,'updated_parsed'):
#                entry_updated = entry.updated_parsed
#                entry_updated = int(calendar.timegm(entry_updated)*1000)
#            
#            if entry_published == None:
#                entry_published = entry_updated
#            if entry_updated == None:
#                entry_updated = entry_published
#            
#            if (
#                item_create or
#                db_item.title != entry.title or
#                db_item.published != entry_published or
#                db_item.updated != entry_updated or
#                db_item.link != entry.link or
#                db_item.content != entry_content
#            ):
#                db_item.title = entry.title
#                db_item.published = entry_published
#                db_item.updated = entry_updated
#                db_item.link = entry.link
#                db_item.content = entry_content
#                db_item.last_detail_update = now
#            
#            db_item.save()
#
#    except AttributeError as e:
#        print e
#        pass


#POLL__RESULT_HTML_REDIRECT = "html_redirect"
#POLL__RESULT_FEED = "feed"
#POLL__RESULT_FAIL = "fail"
#
#
#def poll(url):
#    """return POLL__RESULT_XXX, feedparser_parse, final_url"""
#    
#    redirect = 0
#    while True:
#        feedparser_parse = feedparser.parse(url)
#        ++redirect
#
#        if feedparser_parse['bozo'] == 0:
#            return POLL__RESULT_FEED, feedparser_parse, None
#        
#        f = urllib2.urlopen(url)
        

