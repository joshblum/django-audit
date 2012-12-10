"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User

from audit_alert.models import FlaggedUser

from forum.models import *

import unittest

class AuditTestBase(unittest.TestCase):

    def setUp(self, flags):
        self.flags = dict([(flag, []) for flag in flags])
        self.maxDiff = None
        self.forum, self.thread, self.user = self.setup_forum_objects()


    def setup_forum_objects(self):
        """
            Creates a forum and thread object for testing.
        """

        forum = Forum(title="test-forum", slug="test-forum", description="test forum")
        forum.save()
        
        thread = Thread(forum=forum, title="test_thread")
        thread.save()

        user = User.objects.create(username='user1')
        user.save()

        return forum, thread, user

    def generate_audits(self):
        """
            Default message generates no audit objects.
            Should be overridden by subsequent test methods.
        """
        pass

    def get_flagged_users(self):
        """
            Get monitor results for audit objects that were created.
            Should be overridden by subsequent test methods.
        """
        pass

    def _check_flagged_users(self, *args, **kwargs):
        """
            Assert that the correct users are flagged. 
        """

        for flag_type, flagged_objs in kwargs.items():
            test_objs = FlaggedUser.objects.filter(flag_type=flag_type)

            self.assertEqual(len(test_objs), len(flagged_objs))

            self._test_objects(test_objs, flagged_objs)

    def _test_objects(self, test_objs, objs):
        for test_obj, obj in zip(test_objs, objs):
            
            self.assertEqual(str(test_obj.user), str(obj.user))
            self.assertEqual(str(test_obj.flag_type), str(obj.flag_type))
            self.assertEqual(json.loads(str(test_obj.data)), str(obj.data))
            

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()
        FlaggedUser.objects.all().delete()
