# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from MomohaFeed.models import Feed, Item
import simplejson
import memhttpserver
import os
from threading import Thread
import MomohaFeed
import feedparser

MY_DIR = os.path.dirname(os.path.abspath(__file__))


class SimpleTest(TestCase):
    
    TMP_HTTP_PORT = 10080
    
    def test_feedreader(self):
        
        parse_result = feedparser.parse(MY_DIR+"/test/luzi82.xml")
        
        entry = parse_result.entries[0]
        entry_updated = entry.updated_parsed
        self.assertEqual(4, entry_updated.tm_hour)
        #print entry_updated
        

    def test_j_add_subscription(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        thread = Thread(target=httpServer.handle_request)
        thread.start()
#        time0 = MomohaFeed.now64()
        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
#        time1 = MomohaFeed.now64()
        content=response.content
        result = simplejson.loads(content)
        self.assertIn('subscription_id', result)
        self.assertEqual(True, result['success'])
        

#        too white box
#        db_feed = Feed.objects.get(url=url)
#        self.assertEqual(u'栗子現場直播', db_feed.title)
#        self.assertEqual('http://blog.luzi82.com/', db_feed.link)
#        self.assertLessEqual(time0,db_feed.last_poll)
#        self.assertLessEqual(db_feed.last_poll,time1)
#        poll_time = db_feed.last_poll
#        self.assertEqual(poll_time,db_feed.last_detail_update)
#        
#        
#        db_item = Item.objects.get(key='tag:blogger.com,1999:blog-4722587379660982194.post-4669410140138668459')
#        self.assertEqual(db_feed, db_item.feed)
#        self.assertEqual(poll_time, db_item.last_poll)
#        self.assertEqual(u'もう誰にも頼らない', db_item.title)
#        self.assertEqual(1364789700000, db_item.published)
#        self.assertEqual(1364789887000, db_item.updated) # no ms, issue 20
#        self.assertEqual('http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html', db_item.link)
#        self.assertTrue(db_item.content.startswith(u'<p>舊聞：Google 要放棄 Reader'))
#        self.assertTrue(db_item.content.endswith("/>"))
#        self.assertEqual(poll_time, db_item.last_detail_update)


    def test_j_list_subscription(self):

        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        thread = Thread(target=httpServer.handle_request)
        thread.start()
        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertIn('subscription_id', result)
        subscription_id = result['subscription_id']

        response = client.get("/feed/j_list_subscription/")
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(u'栗子現場直播', result['subscription_list'][0]['title'])
        self.assertEqual(subscription_id, result['subscription_list'][0]['id'])


    def test_j_subscription_list_item(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        thread = Thread(target=httpServer.handle_request)
        thread.start()
        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscription_id = result['subscription_id']
        
        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(u'もう誰にも頼らない', result['item_list'][0]['title'])
        self.assertIn('id', result['item_list'][0])
        self.assertEqual(1364789700000, result['item_list'][0]['published'])
        self.assertEqual('http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html', result['item_list'][0]['link'])
