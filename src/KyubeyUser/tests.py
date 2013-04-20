from django.test import TestCase
from django.test.client import Client
import simplejson
from django.contrib.auth.models import User


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


    def test_verify_login(self):
        
        User.objects.create_user(
            SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        
        
        client = Client()
        
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'verify_login',
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['success'])
        self.assertEqual('not login', result['reason'])
        
        
        client.login(
            username=SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )


        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'verify_login',
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(True, result['success'])
        self.assertEqual(SimpleTest.TEST_USERNAME, result['user']['username'])


    ###

    def test_double_reg_acc(self):

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
        
        self.assertEqual(False, result['success'])
        self.assertEqual('username exist', result['reason'])


    def test_reg_acc_password_short(self):
        
        client = Client()
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'add_user',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': '123',
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['success'])
        self.assertEqual('password short', result['reason'])


    def test_login_username_not_exist(self):
        
        client = Client()
        
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
        
        self.assertEqual(False, result['success'])
        self.assertEqual('login fail', result['reason'])

        
    def test_login_password_error(self):
        User.objects.create_user(
            SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        
        client = Client()
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'login',
            'argv':{
                'username': SimpleTest.TEST_USERNAME,
                'password': SimpleTest.TEST_PASSWORD+'x',
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['success'])
        self.assertEqual('login fail', result['reason'])

    
    def test_set_password_oldpassword_error(self):
        User.objects.create_user(
            SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        client = Client()
        client.login(
            username=SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'user_set_password',
            'argv':{
                'old_password': SimpleTest.TEST_PASSWORD+'x',
                'new_password': SimpleTest.TEST_PASSWORD+'xx',
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['success'])
        self.assertEqual('old_password fail', result['reason'])

    
    def test_set_password_newpassword_short(self):
        User.objects.create_user(
            SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        client = Client()
        client.login(
            username=SimpleTest.TEST_USERNAME,
            password=SimpleTest.TEST_PASSWORD
        )
        
        response = client.post("/users/json/",{'json':simplejson.dumps({
            'cmd':'user_set_password',
            'argv':{
                'old_password': SimpleTest.TEST_PASSWORD,
                'new_password': '123',
            },
        })})
        self.assertEqual(200, response.status_code)
        content = response.content
        result = simplejson.loads(content)
        
        self.assertEqual(False, result['success'])
        self.assertEqual('new_password short', result['reason'])
