# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from MomohaFeed.models import Feed
import simplejson
import memhttpserver
import os
from threading import Thread

MY_DIR = os.path.dirname(os.path.abspath(__file__))


class SimpleTest(TestCase):
    
    TMP_HTTP_PORT = 10080

    def test_j_add_subscription(self):
        
        TMP_HTTP_PORT = SimpleTest.TMP_HTTP_PORT
        url = 'http://localhost:{0}/luzi82.xml'.format(TMP_HTTP_PORT)

        feed = open(MY_DIR+"/test/luzi82.xml").read()
        httpServer = memhttpserver.MemHTTPServer(('localhost',TMP_HTTP_PORT))
        httpServer.set_get_output('/luzi82.xml', 'text/rss', feed)
        httpServer.server_activate()
        thread = Thread(target=httpServer.handle_request)
        thread.start()
        
        User.objects.create_user("user",password="pass")
        
        client = Client()
        client.login(username="user",password="pass")

        response = client.post("/feed/j_add_subscription/",{
            'url':url
        })
        content=response.content
        result = simplejson.loads(content)
        self.assertIn('subscription_id', result)
        
        db_feed = Feed.objects.get(url=url)
        self.assertEqual(u'栗子現場直播', db_feed.title)
        self.assertEqual('http://blog.luzi82.com/', db_feed.link)
