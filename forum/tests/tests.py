from django.utils import unittest
from django.test import Client
from django.contrib.auth.models import User
import random
import cProfile
from forum.models import *

import time

FORUM_ADD = '/admin/forum/forum/add/'
THREAD_ADD = '/admin/forum/thread/add/'
POST_ADD = '/admin/forum/post/add/'

class TestBase(unittest.TestCase):
    def setUp(self):
        try:
            self.user = User.objects.get(id=1) # user is already created.
        except:
            self.user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='1234')
            self.user.is_superuser = True
            self.user.is_staff = True
            self.user.save()

        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        self.client.login(username='john', password='1234')

    def assertAuditCreation(self, obj_type, obj_count, audit_count):
        """
            Assert that the object type was created and that audit logs were created
        """
        self.assertEqual(obj_type.objects.all().count(), obj_count)
        self.assertEqual(obj_type.audit_log.all().count(), audit_count)
        self.assertAuditDetails(obj_type)

    def assertAuditDetails(self, obj_type):
        """
            Assert that audit log details, user information and ip information are created
        """
        for i in obj_type.audit_log.all():
            self.assertEqual(i.action_user.username, "john")
            self.assertEqual(i.action_ip, "127.0.0.1")

class TestForumCreation(TestBase):

    def test_details(self):
        response = self.client.post(FORUM_ADD,
            {
            'title': 'Test', 
            'slug': 'Test', 
            'description': 'Test',
            'parent': '',
            'ordering': '',
            '_save': 'Save'
            })
        self.assertAuditCreation(Forum, 1, 1)

class TestForumThread(TestBase):

    def test_details(self):
        response = self.client.post(THREAD_ADD,
            {
            'forum': '1',
            'title': 'Test 1234',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertAuditCreation(Thread, 1, 1)

class TestForumThread2(TestBase):

    def test_details(self):
        response = self.client.post(THREAD_ADD,
            {
            'forum': '1',
            'title': 'Test 5678',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })

        self.assertAuditCreation(Thread, 2, 2)


class TestForumCreation2(TestBase):

    def test_details(self):
        response = self.client.post(FORUM_ADD, 
            {
            'title': 'Test2', 
            'slug': 'Test2', 
            'description': 'Test2',
            'parent': '',
            'ordering': '',
            '_save': 'Save'
            })

        self.assertAuditCreation(Forum, 2, 2)

class TestForumThread3(TestBase):

    def test_details(self):
        response = self.client.post(THREAD_ADD,
            {
            'forum': '2',
            'title': 'Test 1234',
            'posts': '0',
            'views': '0',
            'latest_post_time_0': time.strftime("%Y-%m-%d"),
            'latest_post_time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertAuditCreation(Thread, 3, 3)

class TestForumThreadPost(TestBase):

    def test_details(self):
        response = self.client.post(POST_ADD,
            {
            'thread': '1',
            'author': '1',
            'body': 'Test',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertAuditCreation(Post, 1, 2)

class TestForumThreadPost2(TestBase):

    def test_details(self):
        response = self.client.post(POST_ADD,
            {
            'thread': '2',
            'author': '1',
            'body': 'Test thread 5678',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertAuditCreation(Post, 2, 4)

class TestForumThreadPost3(TestBase):

    def test_details(self):
        response = self.client.post(POST_ADD,
            {
            'thread': '1',
            'author': '1',
            'body': 'Test thread 1234 on forum 2',
            'time_0': time.strftime("%Y-%m-%d"),
            'time_1': time.strftime("%H:%M:%S"),
            '_save': 'Save'
            })
        self.assertAuditCreation(Post, 3, 6)

class TestForumThreadPostGet(TestBase):

    def test_details(self):
        response = self.client.get('/admin/forum/post/1/') #test that read creates a log entry
        self.assertAuditCreation(Post, 3, 7)
    
