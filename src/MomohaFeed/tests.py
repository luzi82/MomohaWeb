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
import time

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
        httpServer.timeout = 3
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        thread = Thread(target=httpServer.handle_request)
        thread.start()
        # time0 = MomohaFeed.now64()
        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
        # time1 = MomohaFeed.now64()
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertIn('subscription', result)

        self.verify_subscription(result['subscription'])

        self.assertEqual(True, result['success'])
        
        vm_subscription = result['subscription']
        self.assertEqual(u'栗子現場直播', vm_subscription['title'])
        self.assertEqual(u'http://blog.luzi82.com/', vm_subscription['link'])
        self.assertEqual(True, vm_subscription['enable'])

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
        httpServer.timeout = 3
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
        vm_subscription_0 = result['subscription']
#        subscription_id = result['subscription']['id']

        response = client.get("/feed/j_list_subscription/")
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscription_list']))
        for subscription in result['subscription_list']:
            self.verify_subscription(subscription)

        vm_subscription_1 = result['subscription_list'][0]
        self.assertEqual(vm_subscription_0, vm_subscription_1)


    def test_j_subscription_set_enable(self):

        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
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
        vm_subscription = result['subscription']
        subscription_id = result['subscription']['id']
        
        response = client.post("/feed/j_subscription_set_enable/",{
            'subscription_id': subscription_id,
            'value': False
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        response = client.get("/feed/j_list_subscription/")
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(0, len(result['subscription_list']))

        response = client.post("/feed/j_subscription_set_enable/",{
            'subscription_id': subscription_id,
            'value': True
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        response = client.get("/feed/j_list_subscription/")
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscription_list']))
        self.assertEqual(vm_subscription, result['subscription_list'][0])


    def test_j_subscription_list_item(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
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
        subscription_id = result['subscription']['id']
        
        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        for vm_item in result['item_list']:
            self.verify_item(vm_item)
        
        vm_item = result['item_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
        self.assertEqual(1364789700000, vm_item['published'])
        self.assertEqual(
            'http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html',
            vm_item['link']
        )
        self.assertEqual(False,vm_item['readdone'])


    def test_j_subscription_list_item_detail(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
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
        subscription_id = result['subscription']['id']
        
        response = client.post("/feed/j_subscription_list_item_detail/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        for vm_item_detail in result['item_detail_list']:
            self.verify_item_detail(vm_item_detail)
        
        vm_item_detail = result['item_detail_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item_detail['title'])
        self.assertEqual(1364789700000, vm_item_detail['published'])
        self.assertEqual(
            'http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html',
            vm_item_detail['link']
        )
        self.assertTrue(vm_item_detail['content'].startswith(u'<p>舊聞：Google 要放棄 Reader'))
        self.assertTrue(vm_item_detail['content'].endswith("/>"))
        self.assertEqual(False,vm_item_detail['readdone'])


    def test_j_subscription_item_detail(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
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
        subscription_id = result['subscription']['id']


        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(u'もう誰にも頼らない', result['item_list'][0]['title'])
        item_id = result['item_list'][0]['id']


        response = client.post("/feed/j_subscription_item_detail/",{
            'subscription_id': subscription_id,
            'item_id': item_id
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('item_detail',result)
        self.verify_item_detail(result['item_detail'])

        vm_item_detail = result['item_detail']
        self.assertEqual(u'もう誰にも頼らない', vm_item_detail['title'])
        self.assertEqual(1364789700000, vm_item_detail['published'])
        self.assertEqual(
            'http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html',
            vm_item_detail['link']
        )
        self.assertEqual(1364789887000, vm_item_detail['updated'])
        self.assertTrue(vm_item_detail['content'].startswith(u'<p>舊聞：Google 要放棄 Reader'))
        self.assertTrue(vm_item_detail['content'].endswith("/>"))
        self.assertEqual(False,vm_item_detail['readdone'])
        
    
    def test_j_subscription_item_set_readdone(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
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
        subscription_id = result['subscription']['id']
        

        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
        item_id = vm_item['id']
        

        response = client.post("/feed/j_subscription_item_set_readdone/",{
            'subscription_id': subscription_id,
            'item_id': item_id,
            'value': True
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertEqual(True, result['success'])


        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_list'][0])
        self.assertNotEqual(item_id, result['item_list'][0]['id'])


        response = client.post("/feed/j_subscription_item_detail/",{
            'subscription_id': subscription_id,
            'item_id': item_id
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(True, result['item_detail']['readdone'])


        response = client.post("/feed/j_subscription_item_set_readdone/",{
            'subscription_id': subscription_id,
            'item_id': item_id,
            'value': False
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertEqual(True, result['success'])
        
        
        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_list'][0])
        self.assertEqual(item_id, result['item_list'][0]['id'])


        response = client.post("/feed/j_subscription_item_detail/",{
            'subscription_id': subscription_id,
            'item_id': item_id
        })
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['item_detail']['readdone'])
        
    
    def test_j_subscription_poll (self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

        thread = Thread(target=httpServer.handle_request)
        thread.start()

        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])

        feed = open(MY_DIR+"/test/yahoo_hk_rss_1.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

        thread = Thread(target=httpServer.handle_request)
        thread.start()

        response = client.post("/feed/j_subscription_poll/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])

        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][2]
        self.assertEqual(u'馬道立：人大常委會解釋基本法　法院受約束', vm_item['title'])


    def test_update_feed_pool (self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        TEST_URL = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 3
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

        thread = Thread(target=httpServer.handle_request)
        thread.start()

        response = client.post("/feed/j_add_subscription/",{
            'url':TEST_URL
        })
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])

        feed = open(MY_DIR+"/test/yahoo_hk_rss_1.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        # if poll happen, it may block
        MomohaFeed.update_feed_pool(1000)

        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])
        
        time.sleep(1500.0/1000.0)

        thread = Thread(target=httpServer.handle_request)
        thread.start()

        MomohaFeed.update_feed_pool(1000)

        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': subscription_id
        })
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_list'][2]
        self.assertEqual(u'馬道立：人大常委會解釋基本法　法院受約束', vm_item['title'])


    def test_j_subscription_list_item_404(self):

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        response = client.post("/feed/j_subscription_list_item/",{
            'subscription_id': 123
        })
        self.assertEqual(404,response.status_code)


    def test_j_subscription_list_item_detail_404(self):

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        response = client.post("/feed/j_subscription_list_item_detail/",{
            'subscription_id': 123
        })
        self.assertEqual(404,response.status_code)


    def verify_subscription(self,vm_subscription):

        self.assertIn('id', vm_subscription)
        self.assertIn('title', vm_subscription)
        self.assertIn('link', vm_subscription)
        self.assertIn('enable', vm_subscription)


    def verify_subscription_detail(self,vm_subscription_detail):

        self.verify_subscription(vm_subscription_detail)
        self.assertIn('user', vm_subscription_detail)
        self.assertIn('feed_id', vm_subscription_detail)
        self.assertIn('url', vm_subscription_detail)
        self.assertIn('last_poll', vm_subscription_detail)
        self.assertIn('last_detail_update', vm_subscription_detail)


    def verify_item(self,vm_item):

        self.assertIn('id', vm_item)
        self.assertIn('title', vm_item)
        self.assertIn('published', vm_item)
        self.assertIn('link', vm_item)
        self.assertIn('readdone', vm_item)


    def verify_item_detail(self,vm_item_detail):

        self.verify_item(vm_item_detail)
        self.assertIn('feed_id', vm_item_detail)
        self.assertIn('last_poll', vm_item_detail)
        self.assertIn('updated', vm_item_detail)
        self.assertIn('content', vm_item_detail)
        self.assertIn('last_detail_update', vm_item_detail)
