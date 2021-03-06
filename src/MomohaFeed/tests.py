# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
import simplejson
import memhttpserver
import os
from threading import Thread
import MomohaFeed
import feedparser
import time
import enum
from django.core.urlresolvers import reverse
from lxml import etree
import pprint
import xml.sax

MY_DIR = os.path.dirname(os.path.abspath(__file__))


class SimpleTest(TestCase):
    
    TMP_HTTP_PORT = 10080
    
    def test_feedreader(self):

        parse_result = feedparser.parse(MY_DIR+"/test/akibablog.xml")
        self.assertEqual(u"アキバBlog（秋葉原ブログ）",parse_result.feed.title)
        self.assertEqual(u"http://blog.livedoor.jp/geek/",parse_result.feed.link)
        self.assertEqual(15,len(parse_result.entries))
        entry=parse_result.entries[0]
        self.assertEqual(u"くそみそテクニック阿部さんの金玉クッキー“あべたま”　「一度食べたらクセになる！」",entry.title)
        self.assertEqual(u"http://blog.livedoor.jp/geek/archives/51389467.html",entry.link)
        self.assertEqual(u"http://blog.livedoor.jp/geek/archives/51389467.html",entry.id)
        self.assertTrue(entry.content[0].value.startswith("<a href"));
        self.assertTrue(entry.content[0].value.endswith(" />"));
        entry=parse_result.entries[len(parse_result.entries)-1]
        self.assertEqual(u"フォトカノYour Eyes Only２巻  「主人公の変態性が増していくｗ」",entry.title)
        self.assertEqual(u"http://blog.livedoor.jp/geek/archives/51389231.html",entry.link)
        self.assertEqual(u"http://blog.livedoor.jp/geek/archives/51389231.html",entry.id)
        self.assertTrue(entry.content[0].value.startswith("<a href"));
        self.assertTrue(entry.content[0].value.endswith(" />"));
        
        parse_result = feedparser.parse(MY_DIR+"/test/luzi82.xml")
        entry = parse_result.entries[0]
        entry_updated = entry.updated_parsed
        self.assertEqual(4, entry_updated.tm_hour)
        

    def test_j_add_subscription(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)
        # time0 = MomohaFeed.now64()
        #response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            }
        })})
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
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        self.start_server_loop(httpServer)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        vm_subscription_0 = result['subscription']
#        subscription_id = result['subscription']['id']

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscription_list']))
        for subscription in result['subscription_list']:
            self.verify_subscription(subscription)

        vm_subscription_1 = result['subscription_list'][0]
#        self.assertEqual(vm_subscription_0, vm_subscription_1)
        self.assertEqual(vm_subscription_0['id'], vm_subscription_1['id'])
        self.assertEqual(vm_subscription_0['link'], vm_subscription_1['link'])
        self.assertEqual(vm_subscription_0['title'], vm_subscription_1['title'])


#    @skip('skip')
    def test_j_subscription_set_enable(self):

        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        vm_subscription = result['subscription']
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_set_enable',
            'argv':{
                'subscription_id': subscription_id,
                'value': False
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(0, len(result['subscription_list']))

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_set_enable',
            'argv':{
                'subscription_id': subscription_id,
                'value': True
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscription_list']))
        self.assertEqual(vm_subscription['id'], result['subscription_list'][0]['id'])


##    @skip('skip')
#    def test_j_subscription_list_item(self):
#        
#        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
#        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)
#
#        feed = open(MY_DIR+"/test/luzi82.xml").read()
#        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
#        httpServer.timeout = 1
#        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
#        httpServer.server_activate()
#        
#        User.objects.create_user("user",password="pass")
#        
#        client = Client()
#        client.login(username="user",password="pass")
#        
##        thread = Thread(target=httpServer.handle_request)
##        thread.start()
#        self.start_server_loop(httpServer)
#        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
#            'cmd':'add_subscription',
#            'argv':{
#                'url':url,
#            },
#        })})
#        content=response.content
#        result = simplejson.loads(content)
#        self.assertEqual(True, result['success'])
#        subscription_id = result['subscription']['id']
#        
#        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
#            'cmd':'subscription_list_item',
#            'argv':{
#                'subscription_id': subscription_id,
#                'show_readdone'  : False,
#            },
#        })})
#        content=response.content
#        result = simplejson.loads(content)
#
#        for vm_item in result['item_list']:
#            self.verify_item(vm_item)
#        
#        vm_item = result['item_list'][0]
#        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
#        self.assertEqual(1364789700000, vm_item['published'])
#        self.assertEqual(
#            'http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html',
#            vm_item['link']
#        )
#        self.assertEqual(False,vm_item['readdone'])


#    @skip('skip')
    def test_j_subscription_list_item_detail(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
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


#    @skip('skip')
    def test_j_subscription_item_detail(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(u'もう誰にも頼らない', result['item_detail_list'][0]['title'])
        item_id = result['item_detail_list'][0]['id']


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
            },
        })})
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
        
    
#    @skip('skip')
    def test_j_subscription_item_set_readdone(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
        item_id = vm_item['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertNotEqual(item_id, result['item_detail_list'][0]['id'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(True, result['item_detail']['readdone'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertEqual(True, result['success'])
        
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertEqual(item_id, result['item_detail_list'][0]['id'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['item_detail']['readdone'])
        
    
#    @skip('skip')
    def test_j_subscription_poll (self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])

        feed = open(MY_DIR+"/test/yahoo_hk_rss_1.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
#        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_poll',
            'argv':{
                'subscription_id': subscription_id
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][2]
        self.assertEqual(u'馬道立：人大常委會解釋基本法　法院受約束', vm_item['title'])


#    @skip('skip')
    def test_update_feed_pool (self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        TEST_URL = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':TEST_URL,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])

        feed = open(MY_DIR+"/test/yahoo_hk_rss_1.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        MomohaFeed.update_feed_pool(2000)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][2]
        self.assertEqual(u'將軍澳醫院疑似H7N9個案測試結果呈陰性', vm_item['title'])
        
        time.sleep(2500.0/1000.0)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        MomohaFeed.update_feed_pool(2000)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][2]
        self.assertEqual(u'馬道立：人大常委會解釋基本法　法院受約束', vm_item['title'])


#    @skip('skip')
    def test_subscription_all_readdone (self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)
        url1 = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)

#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertGreater(len(result['item_detail_list']), 0)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_all_readdone',
            'argv':{
                'subscription_id': subscription_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(0, len(result['item_detail_list']))
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url1,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(25, len(result['item_detail_list']))
        self.assertIn('now',result)
        #print result['item_detail_list']
        time = result['now']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_all_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'range_first_poll': time-10000,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(25, len(result['item_detail_list']))

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_all_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'range_first_poll': time,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(0, len(result['item_detail_list']))


#    @skip('skip')
    def test_subscription_list_item_show_readdone(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
        item_id = vm_item['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertNotEqual(item_id, result['item_detail_list'][0]['id'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertEqual(item_id, result['item_detail_list'][0]['id'])
        self.assertEqual(True, result['item_detail_list'][0]['readdone'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertNotEqual(item_id, result['item_detail_list'][0]['id'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('id',result['item_detail_list'][0])
        self.assertEqual(item_id, result['item_detail_list'][0]['id'])
        self.assertEqual(True, result['item_detail_list'][0]['readdone'])


#    @skip('skip')
    def test_subscription_detail(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.verify_subscription(result['subscription'])

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.verify_subscription_detail(result['subscription_detail'])

        vm_subscription_detail = result['subscription_detail']
        self.assertEqual(u'栗子現場直播', vm_subscription_detail['title'])
        self.assertEqual(u'http://blog.luzi82.com/', vm_subscription_detail['link'])
        self.assertEqual(True, vm_subscription_detail['enable'])
        self.assertEqual(url, vm_subscription_detail['url'])
    
    
#    @skip('skip')
    def test_subscription_set_star(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        item_id = vm_item['id']
        self.assertEqual(False, vm_item['star'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_star',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('success', result)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        self.assertEqual(item_id, vm_item['id'])
        self.assertEqual(True, vm_item['star'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'item_id'        : item_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['item_detail']['star'])
    
    
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_star',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('success', result)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        self.assertEqual(item_id, vm_item['id'])
        self.assertEqual(False, vm_item['star'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'item_id'        : item_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['item_detail']['star'])
    
    
#    @skip('skip')
    def test_issue_34(self):
        '''Item, show only Item.last_poll > Subscription.start'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        feed_id = result['subscription_detail']['feed_id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        exist = False
        for item in result['item_detail_list']:
            exist = exist or ( item['title'] == u"年內查6500幢大廈消防" )
        self.assertTrue(exist)
    
        exist = False
        for item in result['item_detail_list']:
            exist = exist or ( item['title'] == u"六十五歲女子李瑞琼失蹤" )
        self.assertTrue(exist)
    
        User.objects.create_user("user0",password="pass0")
        
        client = Client()
        client.login(username="user0",password="pass0")

        feed = open(MY_DIR+"/test/yahoo_hk_rss_1.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        self.assertNotEqual(subscription_id, result['subscription']['id'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(feed_id, result['subscription_detail']['feed_id'])
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        exist = False
        for item in result['item_detail_list']:
            exist = exist or ( item['title'] == u"年內查6500幢大廈消防" )
        self.assertFalse(exist) # issue 34

        exist = False
        for item in result['item_detail_list']:
            exist = exist or ( item['title'] == u"六十五歲女子李瑞琼失蹤" )
        self.assertTrue(exist)


#    @skip('skip')
    def test_issue_21(self):
        '''add subscription, bad URL handling'''
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':"invalid_url",
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_URL, result['fail_reason'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':"http://",
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_URL, result['fail_reason'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':"http:/www.google.com",
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_URL, result['fail_reason'])


#    @skip('skip')
    def test_issue_23(self):
        '''add subscription, non feed handling'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        # server not exist
        print "server not exist"
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_FEED_SOURCE, result['fail_reason'])
        
        # server timeout
        print "server timeout"

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_FEED_SOURCE, result['fail_reason'])

        # 404
        print "404"

#        server_thread = self.start_server_loop(httpServer)

#        httpServer.set_get_output('/test.xml', status=404)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_FEED_SOURCE, result['fail_reason'])
        
        # non-feed
        print "non-feed"

        feed = open(MY_DIR+"/test/year_wish.jpg").read()
        httpServer.set_get_output('/test.xml', 'image/jpeg', feed)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_FEED_SOURCE, result['fail_reason'])
        
        # parse error
        print "parse error"
        
        feed = open(MY_DIR+"/test/luzi82.html").read()
        httpServer.set_get_output('/test.xml', 'text/html', feed)
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(False, result['success'])
        self.assertEqual(enum.FailReason.BAD_FEED_SOURCE, result['fail_reason'])
        
#        server_thread.join()


#    @skip('skip')
    def test_issue_22(self):
        '''add subscription, web page handling'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test0.xml'.format(TMP_HTTP_PORT)
        url2 = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.server_activate()

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        feed = open(MY_DIR+"/test/luzi82_blog_atom.html").read()
        httpServer.set_get_output('/test0.xml', 'text/html', feed)
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']

        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(url2, result['subscription_detail']['url'])
        self.assertEqual(u'栗子現場直播', result['subscription_detail']['title'])
        self.assertEqual(u'http://blog.luzi82.com/', result['subscription_detail']['link'])
        self.assertEqual(True, result['subscription_detail']['enable'])
        
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        vm_item = result['item_detail_list'][0]
        self.assertEqual(u'もう誰にも頼らない', vm_item['title'])
        self.assertEqual(1364789700000, vm_item['published'])
        self.assertEqual(
            'http://feedproxy.google.com/~r/luzi82_blog/~3/4wZwEC07FCY/blog-post_6399.html',
            vm_item['link']
        )
        self.assertEqual(False,vm_item['readdone'])


##    @skip('skip')
#    def test_j_subscription_list_item_404(self):
#
#        User.objects.create_user("user",password="pass")
#        
#        client = Client()
#        client.login(username="user",password="pass")
#
#        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
#            'cmd':'subscription_list_item',
#            'argv':{
#                'subscription_id': 123,
#                'show_readdone'  : False,
#            },
#        })})
#        self.assertEqual(404,response.status_code)


#    @skip('skip')
    def test_j_subscription_list_item_detail_404(self):

        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': 123,
                'show_readdone'  : False,
            },
        })})
        self.assertEqual(404,response.status_code)


    def test_issue_40(self):
        '''module_subscription.load should be lazy'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        self.start_server_loop(httpServer)
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id'   : subscription_id,
                'show_readdone'     : False,
                'range_published'   : None,
                'range_id'          : None,
                'item_count'        : 3,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        
        self.assertEqual(3, len(result['item_detail_list']))
        self.assertEqual(u'もう誰にも頼らない', result['item_detail_list'][0]['title'])
        self.assertEqual(u'團結', result['item_detail_list'][1]['title'])
        self.assertEqual(u'最後に残った道しるべ', result['item_detail_list'][2]['title'])
        
        next_range_published = result['item_detail_list'][2]['published']
        next_range_id = result['item_detail_list'][2]['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id'   : subscription_id,
                'show_readdone'     : False,
                'range_published'   : next_range_published,
                'range_id'          : next_range_id,
                'item_count'        : 3,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(3, len(result['item_detail_list']))
        self.assertEqual(u'國旗與狗不准燃燒', result['item_detail_list'][0]['title'])
        self.assertEqual(u'水無灯里生日 (-273歲)', result['item_detail_list'][1]['title'])
        self.assertEqual(u'有一個月沒有寫 blog 了', result['item_detail_list'][2]['title'])
        
        next_range_published = result['item_detail_list'][2]['published']
        next_range_id = result['item_detail_list'][2]['id']
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id'   : subscription_id,
                'show_readdone'     : False,
                'range_published'   : next_range_published,
                'range_id'          : next_range_id,
                'item_count'        : 30,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(19, len(result['item_detail_list']))
        self.assertEqual(u'Mikupa 香港攻略', result['item_detail_list'][0]['title'])
        self.assertEqual(u'相睇云云', result['item_detail_list'][18]['title'])

        
    def test_issue_112(self):
        '''Subscription custom name'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_set_title',
            'argv':{
                'subscription_id': subscription_id,
                'value': 'asdf',
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
            'argv':{},
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(u'asdf', result['subscription_list'][0]['title'])
#        self.assertEqual(u'栗子現場直播', result['subscription_list'][0]['feed_title'])
#        self.assertEqual(u'asdf', result['subscription_list'][0]['subscription_title'])
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id': subscription_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(u'asdf', result['subscription_detail']['title'])
        self.assertEqual(u'栗子現場直播', result['subscription_detail']['feed_title'])
        self.assertEqual(u'asdf', result['subscription_detail']['subscription_title'])


    def test_issue_50(self):
        '''Subscription tag management'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscriptiontag',
            'argv':{
                'title':'9WjaWarN',
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        subscriptiontag_id = result['subscriptiontag']['id']
        
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontag_detail',
            'argv':{
                'subscriptiontag_id':subscriptiontag_id,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual('9WjaWarN', result['subscriptiontag_detail']['title'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscriptiontag_list']))
        self.assertEqual('9WjaWarN', result['subscriptiontag_list'][0]['title'])
        self.assertEqual(subscriptiontag_id, result['subscriptiontag_list'][0]['id'])
        
 
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontag_set_title',
            'argv':{
                'subscriptiontag_id':subscriptiontag_id,
                'title':'EdJO5ZL8',
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])

       
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscriptiontag_list']))
        self.assertEqual('EdJO5ZL8', result['subscriptiontag_list'][0]['title'])
        self.assertEqual(subscriptiontag_id, result['subscriptiontag_list'][0]['id'])

        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontagsubscription_set',
            'argv':{
                'set_list':[{
                    'subscriptiontag_id': subscriptiontag_id,
                    'subscription_id': subscription_id,
                    'enable': True,
                }],
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(1, len(result['subscriptiontagsubscriptionrelation_list']))
        self.assertEqual(subscriptiontag_id, result['subscriptiontagsubscriptionrelation_list'][0]['subscriptiontag_id'])
        self.assertEqual(subscription_id, result['subscriptiontagsubscriptionrelation_list'][0]['subscription_id'])
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontag_list_item_detail',
            'argv':{
                'subscriptiontag_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(u'もう誰にも頼らない', result['item_detail_list'][0]['title'])

        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontagsubscription_set',
            'argv':{
                'set_list':[{
                    'subscriptiontag_id': subscriptiontag_id,
                    'subscription_id': subscription_id,
                    'enable': False,
                }],
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(0, len(result['subscriptiontagsubscriptionrelation_list']))


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscriptiontag_set_enable',
            'argv':{
                'subscriptiontag_id':subscriptiontag_id,
                'enable':False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(0, len(result['subscriptiontag_list']))


    def test_issue_106(self):
        '''google reader import'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        feed = open(MY_DIR+"/test/yahoo_hk_rss_0.xml").read()
        httpServer.set_get_output('/yahoo.xml', 'text/rss', feed)
        feed = open(MY_DIR+"/test/rico.xml").read()
        httpServer.set_get_output('/rico.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
        
        opml = open(MY_DIR+"/test/opml.xml")
        response = client.post(reverse('MomohaFeed.views.upload'),{
            'json': simplejson.dumps({
                'cmd':'import_opml',
            }),
            'file': opml
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
    

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(3, len(result['subscription_list']))
        self.assertEqual(u'title0', result['subscription_list'][0]['title'])
        subscription0_id = result['subscription_list'][0]['id']
        self.assertEqual(u'title1', result['subscription_list'][1]['title'])
        subscription1_id = result['subscription_list'][1]['id']
        self.assertEqual(u'title2', result['subscription_list'][2]['title'])

        self.assertEqual(1, len(result['subscriptiontag_list']))
        self.assertEqual(u'tag0', result['subscriptiontag_list'][0]['title'])
        subscriptiontag_id = result['subscriptiontag_list'][0]['id']

        self.assertEqual(2, len(result['subscriptiontagsubscriptionrelation_list']))
        self.assertEqual(subscriptiontag_id, result['subscriptiontagsubscriptionrelation_list'][0]['subscriptiontag_id'])
        self.assertEqual(subscription0_id, result['subscriptiontagsubscriptionrelation_list'][0]['subscription_id'])
        self.assertEqual(subscriptiontag_id, result['subscriptiontagsubscriptionrelation_list'][1]['subscriptiontag_id'])
        self.assertEqual(subscription1_id, result['subscriptiontagsubscriptionrelation_list'][1]['subscription_id'])

        
    def test_azumakiyohiko(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/azumakiyohiko.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        feed = open(MY_DIR+"/test/azumakiyohiko.xml").read()
        httpServer.set_get_output('/azumakiyohiko.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])

    
    def test_azumakiyohiko_x(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/azumakiyohiko.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        feed = open(MY_DIR+"/test/azumakiyohiko_x.xml").read()
        httpServer.set_get_output('/azumakiyohiko.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        

    def test_azumakiyohiko_x2(self):
        print "azumakiyohiko_x.xml"
        feedparser.parse(MY_DIR+"/test/azumakiyohiko_x.xml")
        print "azumakiyohiko.xml"
        feedparser.parse(MY_DIR+"/test/azumakiyohiko.xml")


    def test_azumakiyohiko_rss(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/azumakiyohiko.rss.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])


    def test_178_rss(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/178.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])

    
    def test_passiontimes_rss(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/test.xml'.format(TMP_HTTP_PORT)

        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        feed = open(MY_DIR+"/test/passiontimes.xml").read()
        httpServer.set_get_output('/test.xml', 'text/rss', feed)
        httpServer.server_activate()
        self.start_server_loop(httpServer)
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")


        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url
            },
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertEqual(True, result['success'])
        
        
    def test_54_tdd (self):
        '''subscription list, add unread count'''
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")
        
#        thread = Thread(target=httpServer.handle_request)
#        thread.start()
        self.start_server_loop(httpServer)

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        subscription_id = result['subscription']['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertIn('unread_count', result['subscription_list'][0])
        self.assertEqual(25, result['subscription_list'][0]['unread_count'])

        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_list_item_detail',
            'argv':{
                'subscription_id': subscription_id,
                'show_readdone'  : False,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        item_id = result['item_detail_list'][0]['id']
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_item_set_readdone',
            'argv':{
                'subscription_id': subscription_id,
                'item_id': item_id,
                'value': True,
            },
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(True, result['success'])
        
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'list_subscription',
        })})
        content=response.content
        result = simplejson.loads(content)

        self.assertEqual(24, result['subscription_list'][0]['unread_count'])

    def test_130(self):
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
 
        url0 = 'http://localhost:{0}/0.xml'.format(TMP_HTTP_PORT)
        url1 = 'http://localhost:{0}/1.xml'.format(TMP_HTTP_PORT)
         
        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.timeout = 1
        httpServer.set_get_output('/0.xml', 'text/rss', feed)
        httpServer.set_get_output('/1.xml', 'text/rss', feed)
        httpServer.server_activate()
         
        User.objects.create_user("user",password="pass")
         
        client = Client()
        client.login(username="user",password="pass")
 
        self.start_server_loop(httpServer)
         
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url0,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertIn('success', result)
        self.assertIn('subscription', result)
        self.assertEqual(True, result['success'])
        subscription_id0 = result['subscription']['id']
 
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'add_subscription',
            'argv':{
                'url':url1,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertIn('success', result)
        self.assertIn('subscription', result)
        self.assertEqual(True, result['success'])
        subscription_id1 = result['subscription']['id']
 
        MomohaFeed.update_feed_pool(0)
         
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id0,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        last_poll0 = result['subscription_detail']['last_poll']
 
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id1,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        last_poll1 = result['subscription_detail']['last_poll']
         
        httpServer.set_get_output('/0.xml', None, None, 404)
 
        time.sleep(0.01)
 
        MomohaFeed.update_feed_pool(0)
 
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id0,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertGreater(result['subscription_detail']['last_poll'],last_poll0) # issue 130
 
        response = client.post(reverse('MomohaFeed.views.json'),{'json':simplejson.dumps({
            'cmd':'subscription_detail',
            'argv':{
                'subscription_id':subscription_id1,
            }
        })})
        content=response.content
        result = simplejson.loads(content)
        self.assertGreater(result['subscription_detail']['last_poll'],last_poll1)

#    def test_azumakiyohiko_x3(self):
#        print "azumakiyohiko_x.xml"
#        f = feedparser._open_resource(
#            MY_DIR+"/test/azumakiyohiko_x.xml",
#            etag=None,
#            modified=None,
#            agent=None,
#            referrer=None,
#            handlers=[],
#            request_headers={}
#        )
#        data = f.read()
#        print data
#
#
#    def test_azumakiyohiko_x4(self):
#        print "azumakiyohiko_x.xml"
#        parse_result = feedparserx.parse(MY_DIR+"/test/azumakiyohiko_x.xml")
#        self.assertTrue(( not parse_result.has_key('version') ) or ( parse_result['version'] == '' ))
#        parse_result = feedparserx.parse(MY_DIR+"/test/luzi82.xml")
#        self.assertTrue(not ( not parse_result.has_key('version') ) or ( parse_result['version'] == '' ))
#        self.assertEqual(u'栗子現場直播',parse_result.feed.title)
#
#    def test_azumakiyohiko_x5(self):
#        print "azumakiyohiko_x.xml"
#        
#        f=open(MY_DIR+"/test/azumakiyohiko_x.xml")
##        data=f.read()
#        
#        saxparser = xml.sax.make_parser([])
#        saxparser.setFeature(xml.sax.handler.feature_namespaces, 1)
#        try:
#            # disable downloading external doctype references, if possible
#            saxparser.setFeature(xml.sax.handler.feature_external_ges, 0)
#        except xml.sax.SAXNotSupportedException:
#            pass
##        saxparser.setContentHandler(feedparser)
##        saxparser.setErrorHandler(feedparser)
#        source = xml.sax.xmlreader.InputSource()
#        source.setByteStream(f)
#        try:
#            print "XxnjwiFj"
#            saxparser.parse(source)
#            print "4A0R4dVV"
#        except xml.sax.SAXException, e:
#            pass
        
        
    ##########
    
    def now64(self):
        ret = time.time()
        ret *= 1000
        ret = int(ret)
        return ret
    

    def start_server_loop(self, httpServer):
        self.httpServer = httpServer
        self.server_run = True
        def loop():
            while(self.server_run):
                try:
                    httpServer.handle_request()
                except:
                    pass
        thread = Thread(target=loop)
        thread.start()
        self.server_thread = thread
        return thread
    
    
    def setUp(self):
        self.server_run = False
        self.server_thread = None
        self.httpServer = None

    
    def tearDown(self):
        self.server_run = False
        if self.server_thread != None :
            self.server_thread.join()
            self.server_thread = None
        if self.httpServer != None:
            if self.httpServer.socket != None:
                self.httpServer.socket.close()
            self.httpServer = None


    ##########

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
        self.assertIn('star', vm_item)


    def verify_item_detail(self,vm_item_detail):

        self.verify_item(vm_item_detail)
        self.assertIn('feed_id', vm_item_detail)
        self.assertIn('last_poll', vm_item_detail)
        self.assertIn('updated', vm_item_detail)
        self.assertIn('content', vm_item_detail)
        self.assertIn('last_detail_update', vm_item_detail)
