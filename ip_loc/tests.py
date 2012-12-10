"""
    File to test the monitor users functionality.
    File creates audit-log objects from various countries and verifies the output of the emails sent
"""

from django.test import Client
from django.db import models
from django.utils import simplejson as json

from ip_loc.cron_tasks.download_tor import DownloadTor
from ip_loc.cron_tasks.download_ip import DownloadIP
from ip_loc.cron_tasks.monitor_users import *
from ip_loc.models import FlaggedUser

from forum.models import *

import unittest

TEST_IP_ADDR = ['199.126.148.30','178.253.68.175','31.40.117.110','18.228.1.190' ] #mapping of countries to ips for testing
# {
#     'CA' : '199.126.148.30',
#     'SY' : '178.253.68.175',
#     'RU' : '31.40.117.110',
#     'US' : '18.228.1.190',
# }

TEST_TOR_ADDR = ['18.228.0.188', '2.29.81.63', '100.1.58.105',] #random tor nodes to be used for testing

class MonitorTestBase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.setup_ip_addr()
        self.setup_tor_addr()
        self.forum, self.thread, self.user = self.setup_forum_objects()
        self.generate_audits()
        self.get_flagged_users()

    def setup_ip_addr(self):
        """
            Download and populate the IP to country database with static downloaded file.
        """
        ip = DownloadIP('ip_loc/test_files/IpToCountry.csv.zip')
        ip.run()

    def setup_tor_addr(self):
        """
            Load the tor list with a static file since the server is rate limited
        """
        tor = DownloadTor('ip_loc/test_files/tor_list.txt')
        tor.run()

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
        """
        user_monitor = MonitorUsers()
        user_monitor.run()

    def _check_flagged_users(self, flagged_countries=[], flagged_tor=[]):
        """
            Assert that the correct users are flagged. 
        """
        
        test_countries = FlaggedUser.objects.filter(flag_type=COUNTRY_FLAG)
        test_tor = FlaggedUser.objects.filter(flag_type=TOR_FLAG)

        self.assertEqual(len(test_countries), len(flagged_countries))

        self.assertEqual(len(test_tor), len(flagged_tor))

        self._test_objects(test_countries, flagged_countries)
        self._test_objects(test_tor, flagged_tor)

    def _test_objects(self, test_objs, objs):
        for test_obj, obj in zip(test_objs, objs):
            
            self.assertEqual(str(test_obj.user), str(obj.user))
            self.assertEqual(str(test_obj.flag_type), str(obj.flag_type))
            self.assertEqual(str(test_obj.data), str(obj.data))
            

    def set_log_entry(self, obj, ip):
        self._change_ip(obj, ip)
        self._change_user(obj, self.user)

    def _change_ip(self, obj, ip):
        """
            Takes an AuditLogObject and changes the action_ip to the given ip.
        """
        obj.action_ip = ip
        obj.save()
        return obj

    def _change_user(self, obj, user):
        """
            Sets the user of the object
        """
        obj.action_user = user
        obj.save()
        return obj

    def tearDown(self):
        Post.objects.all().delete()
        self.user.delete()
        FlaggedUser.objects.all().delete()

class TestNoAudits(MonitorTestBase):
    """
        Tests with no audits that empty lists are returned
    """
    def test(self):
        self._check_flagged_users()

class TestAuditsNoFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects but no audits. All ips are from the same country, no IPs are tor nodes.
        """
        post = Post(thread=self.thread, body="test_body", author=self.user)
        post.save()
        
    def test(self):
        self._check_flagged_users()

class TestAuditsCountryFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects and changes to use different country ips to generate a country flag
        """
        post = Post(thread=self.thread, body="test_body", author=self.user)
        post.save()

        for obj, ip in zip(post.audit_log.all(), TEST_IP_ADDR):
            self.set_log_entry(obj, ip)
    
    def test(self):

        country_data = {'CA': ['199.126.148.30'], 'SY': ['178.253.68.175']}
        country_flags = [
            FlaggedUser(user=self.user, flag_type=COUNTRY_FLAG, data=json.dumps(country_data))
        ]

        self._check_flagged_users(country_flags, [])

class TestAuditsTorFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects and modfy the entry log to reflect a tor node to generate a tor flag
        """
        post = Post(thread=self.thread, body="test_body", author=self.user)
        post.save()

        log_entry = post.audit_log.all()[0]
        self.set_log_entry(log_entry, TEST_TOR_ADDR[0])

    def test(self):
        tor_data = ["18.228.0.188"]
        tor_flags = [
            FlaggedUser(user=self.user, flag_type=TOR_FLAG, data=json.dumps(tor_data))
        ]

        self._check_flagged_users([], tor_flags)

class TestAuditsCountryAndTorFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects for both country and tor flags to be generated. 
        """
        post = Post(thread=self.thread, body="test_body", author=self.user)
        post.save()

        for obj, ip in zip(post.audit_log.all(), TEST_TOR_ADDR):
            self.set_log_entry(obj, ip)

    def test(self):

        country_data = {"GB": ["2.29.81.63"], "US": ["18.228.0.188"]}
        country_flags = [
            FlaggedUser(user=self.user, flag_type=COUNTRY_FLAG, data=json.dumps(country_data))
        ]

        tor_data = ["18.228.0.188", "2.29.81.63",]
        tor_flags = [
            FlaggedUser(user=self.user, flag_type=TOR_FLAG, data=json.dumps(tor_data))
        ]
        self._check_flagged_users(country_flags, tor_flags)