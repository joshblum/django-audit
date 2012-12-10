"""
    File to test the monitor users functionality.
    File creates audit-log objects from various countries and verifies the output of the emails sent
"""

from django.utils import simplejson as json

from ip_loc.cron_tasks.download_tor import DownloadTor
from ip_loc.cron_tasks.download_ip import DownloadIP
from ip_loc.cron_tasks.monitor_users import MonitorUsers, TOR_FLAG, COUNTRY_FLAG

from audit_alert.models import FlaggedUser
from audit_alert.tests import AuditTestBase

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

class MonitorTestBase(AuditTestBase):

    def setUp(self):
        super(MonitorTestBase, self).setUp([COUNTRY_FLAG, TOR_FLAG])
        self.setup_ip_addr()
        self.setup_tor_addr()
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
        user_monitor = MonitorUsers([COUNTRY_FLAG, TOR_FLAG])
        user_monitor.run()
            

    def set_log_entry(self, obj, ip):
        obj.action_ip = ip
        obj.action_user = self.user

        obj.save()

class TestNoAudits(MonitorTestBase):
    """
        Tests with no audits that empty lists are returned
    """
    def test(self):
        self._check_flagged_users(self.flags)

class TestAuditsNoFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects but no audits. All ips are from the same country, no IPs are tor nodes.
        """
        post = self.create_post()
        
    def test(self):
        self._check_flagged_users(self.flags)

class TestAuditsCountryFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects and changes to use different country ips to generate a country flag
        """
        post = self.create_post()

        for obj, ip in zip(post.audit_log.all(), TEST_IP_ADDR):
            self.set_log_entry(obj, ip)
    
    def test(self):

        country_data = {'CA': ['199.126.148.30'], 'SY': ['178.253.68.175']}
        country_flags = [
            FlaggedUser(user=self.user, flag_type=COUNTRY_FLAG, data=json.dumps(country_data))
        ]

        self._check_flagged_users({
            COUNTRY_FLAG : country_flags,
            TOR_FLAG :  [],
            })
class TestAuditsTorFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects and modfy the entry log to reflect a tor node to generate a tor flag
        """
        post = self.create_post()

        log_entry = post.audit_log.all()[0]
        self.set_log_entry(log_entry, TEST_TOR_ADDR[0])

    def test(self):
        tor_data = ["18.228.0.188"]
        tor_flags = [
            FlaggedUser(user=self.user, flag_type=TOR_FLAG, data=json.dumps(tor_data))
        ]

        self._check_flagged_users({
            COUNTRY_FLAG : [],
            TOR_FLAG :  tor_flags,
            })

class TestAuditsCountryAndTorFlags(MonitorTestBase):

    def generate_audits(self):
        """
            Generate audit objects for both country and tor flags to be generated. 
        """
        post = self.create_post()

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
        self._check_flagged_users({
            COUNTRY_FLAG : country_flags,
            TOR_FLAG :  tor_flags,
            })