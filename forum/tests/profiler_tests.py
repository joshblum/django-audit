import cProfile
import random
import time

from test_base import TestBase, FORUM_ADD, THREAD_ADD, POST_BASE, POST_ADD


BASE_PATH = 'forum/tests/profiling/'

class TestProfiler(TestBase):
    
    def create_forums(self):
        for i in range(0,5):
            response = self.client.post(FORUM_ADD,
                {
                'title': 'Test', 
                'slug': 'Test', 
                'description': 'Test',
                'parent': '',
                'ordering': '',
                '_save': 'Save'
                })      
    def create_threads(self):  
        for i in range(1,5):
            response = self.client.post(THREAD_ADD,
                {
                'forum': "'" + str(int(random.uniform(1,5))) + "'",
                'title': 'Test',
                'posts': '0',
                'views': '0',
                'latest_post_time_0': time.strftime("%Y-%m-%d"),
                'latest_post_time_1': time.strftime("%H:%M:%S"),
                '_save': 'Save'
                })
    def create_posts(self):
        for i in xrange(1,2000):
            response = self.client.post(POST_ADD,
                {
                'thread': "'" + str(int(random.uniform(1,5))) + "'",
                'author': '1',
                'body': 'Test',
                'time_0': time.strftime("%Y-%m-%d"),
                'time_1': time.strftime("%H:%M:%S"),
                '_save': 'Save'
                })
    def check_posts(self):
        for i in xrange(1,2000):
            response = self.client.get('/admin/forum/post/' + str(i) + '/')

    def _details(self):
        cProfile.runctx("self.create_forums()", globals(), locals(), "%sbulk_stats-forums.txt"%BASE_PATH)
        cProfile.runctx("self.create_threads()", globals(), locals(), "%sbulk_stats-threads.txt"%BASE_PATH)
        cProfile.runctx("self.create_posts()", globals(), locals(), "%sbulk_stats-posts.txt"%BASE_PATH)
        cProfile.runctx("self.check_posts()", globals(), locals(), "%sbulk_stats-posts-get.txt"%BASE_PATH)