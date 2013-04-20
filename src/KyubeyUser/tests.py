from django.test import TestCase
from django.test.client import Client
import simplejson


class SimpleTest(TestCase):
    
    TEST_USERNAME = 'Kyubey'
    TEST_PASSWORD = 'incubator'

    def test_reg_acc(self):
        """MomohaWeb issue 35: json reg account"""
        
        client = Client()
        
        self.assertNotIn('_auth_user_id', client.session)
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'add_user',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('_auth_user_id', client.session)


    def test_login(self):

        client = Client()
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'add_user',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertTrue(result['success'])


        client = Client()
        
        self.assertNotIn('_auth_user_id', client.session)

        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'login',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)

        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('_auth_user_id', client.session)


    def test_logout(self):
        
        client = Client()
        
        self.assertNotIn('_auth_user_id', client.session)
        

        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'add_user',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertTrue(result['success'])


        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'logout',
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)

        self.assertTrue(result['success'])
        self.assertNotIn('_auth_user_id', client.session)


    def test_user_set_password(self):
        
        password2 = SimpleTest.TEST_PASSWORD+'x'
        
        client = Client()
        
        self.assertNotIn('_auth_user_id', client.session)
        

        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'add_user',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertTrue(result['success'])


        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'user_set_password',
            'argv':{
                'old_password': SimpleTest.TEST_PASSWORD,
                'new_password': password2,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertTrue(result['success'])


        client = Client()
        self.assertNotIn('_auth_user_id', client.session)


        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'login',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertFalse(result['success'])


        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'login',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': password2,
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertIn('success', result)
        self.assertTrue(result['success'])
        self.assertIn('_auth_user_id', client.session)
