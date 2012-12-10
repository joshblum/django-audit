from forum.models import *

import time

from test_base import TestBase

FORUM_ADD = '/admin/forum/forum/add/'
THREAD_ADD = '/admin/forum/thread/add/'
POST_ADD = '/admin/forum/post/add/'

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