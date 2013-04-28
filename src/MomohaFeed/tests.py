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
        self.assertEqual(vm_subscription_0, vm_subscription_1)


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
        self.assertEqual(vm_subscription, result['subscription_list'][0])


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
        self.assertEqual(u'もう誰にも頼らない', result['item_detail_list'][0].title)
        self.assertEqual(u'團結', result['item_detail_list'][1].title)
        self.assertEqual(u'最後に残った道しるべ', result['item_detail_list'][2].title)
        
        next_range_published = result['item_detail_list'][2].published
        next_range_id = result['item_detail_list'][2].id
        

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
        self.assertEqual(u'國旗與狗不准燃燒', result['item_detail_list'][0].title)
        self.assertEqual(u'水無灯里生日 (-273歲)', result['item_detail_list'][1].title)
        self.assertEqual(u'有一個月沒有寫 blog 了', result['item_detail_list'][2].title)
        
        next_range_published = result['item_detail_list'][2].published
        next_range_id = result['item_detail_list'][2].id
        

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

        self.assertEqual(18, len(result['item_detail_list']))
        self.assertEqual(u'Mikupa 香港攻略', result['item_detail_list'][0].title)
        self.assertEqual(u'相睇云云', result['item_detail_list'][17].title)


    ##########
    
    def now64(self):
        ret = time.time()
        ret *= 1000
        ret = int(ret)
        return ret
    

    def start_server_loop(self, httpServer):
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

    
    def tearDown(self):
        self.server_run = False
        if self.server_thread != None :
            self.server_thread.join()
            self.server_thread = None


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
