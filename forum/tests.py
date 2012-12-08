from django.utils import unittest
from django.test import Client
from django.contrib.auth.models import User
import time
import profiler
from forum.models import *

# class TestGet(unittest.TestCase):
#     def setUp(self):
#         user = User.objects.create_user('john', 'johnpassword')
#         user.set_password("1234")
#         user.save()
#         self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
#         self.client.login(username='john', password='1234')

#     def test_details(self):
#         response = self.client.get('/admin/forum/forum/add/', {'title': 'Test', 'slug': 'Test', 'description': 'Test'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['customers']), 5)

class TestBase(unittest.TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='1234')
        user.is_superuser = True
        user.is_staff = True
        user.save()

class TestForumCreation(TestBase):
    def setUp(self):
        super(TestForumCreation, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/forum/add/', 
            {
            'title': 'Test', 
            'slug': 'Test', 
            'description': 'Test',
            'parent': '',
            'ordering': '',
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Forum.objects.all()), 1)
        self.assertEqual(len(Forum.audit_log.all()), 1)

class TestForumThread(unittest.TestCase):
    def setUp(self):
        #super(TestForumThread, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/thread/add/',
            {
            'forum': '1',
            'title': 'Test 1234',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Thread.objects.all()), 1)
        self.assertEqual(len(Thread.audit_log.all()), 1)

class TestForumThread2(unittest.TestCase):
    def setUp(self):
        #super(TestForumThread2, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/thread/add/',
            {
            'forum': '1',
            'title': 'Test 5678',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Thread.objects.all()), 2)
        self.assertEqual(len(Thread.audit_log.all()), 2)

class TestForumCreation2(unittest.TestCase):
    def setUp(self):
        #super(TestForumCreation2, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/forum/add/', 
            {
            'title': 'Test2', 
            'slug': 'Test2', 
            'description': 'Test2',
            'parent': '',
            'ordering': '',
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Forum.objects.all()), 2)
        self.assertEqual(len(Forum.audit_log.all()), 2)

class TestForumThread3(unittest.TestCase):
    def setUp(self):
        #super(TestForumThread3, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/thread/add/',
            {
            'forum': '2',
            'title': 'Test 1234',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Thread.objects.all()), 3)
        self.assertEqual(len(Thread.audit_log.all()), 3)

class TestForumThreadPost(unittest.TestCase):
    def setUp(self):
        #super(TestForumPost, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        print self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/post/add/',
            {
            'thread': '1',
            'author': '1',
            'body': 'Test',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertEqual(len(Post.audit_log.all()), 2)

class TestForumThreadPost2(unittest.TestCase):
    def setUp(self):
        #super(TestForumPost, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        print self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/post/add/',
            {
            'thread': '2',
            'author': '1',
            'body': 'Test thread 5678',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Post.objects.all()), 2)
        self.assertEqual(len(Post.audit_log.all()), 4)

class TestForumThreadPost3(unittest.TestCase):
    def setUp(self):
        #super(TestForumPost, self).setUp()
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        print self.client.login(username='john', password='1234')

    def test_details(self):
        response = self.client.post('/admin/forum/post/add/',
            {
            'thread': '1',
            'author': '1',
            'body': 'Test thread 1234 on forum 2',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Post.objects.all()), 3)
        self.assertEqual(len(Post.audit_log.all()), 6)