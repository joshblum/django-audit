"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client
from django.db import models
from django.utils import simplejson as json

from xss_detect.cron_tasks.xss_parser import XSSParser, XSS_FLAG

from audit_alert.tests import AuditTestBase
from audit_alert.models import FlaggedUser

from forum.models import *

import unittest

TEST_XSS_INPUT = ["?user=<script>alert(document.cookie)</script>", "3f757365723d3c7363726970743e616c65727428646f63756d656e742e636f6f6b6965293c2f7363726970743e22"]

class XSSParserTestBase(AuditTestBase):

    def setUp(self):
        super(XSSParserTestBase, self).setUp([XSS_FLAG])
        self.generate_audits()
        self.get_flagged_users()

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
        parser = XSSParser([XSS_FLAG])
        parser.run()

    def set_log_entry(self, obj, url, get, post):
        obj.action_request_url = url
        obj.action_get_params = get
        obj.action_post_params = post

        obj.save()

    def generic_t_est(self):

        xss_data = TEST_XSS_INPUT
        xss_flags = [
            FlaggedUser(user=self.user, flag_type=XSS_FLAG, data=json.dumps(xss_data))
        ]

        self._check_flagged_users({
            XSS_FLAG : xss_flags,
            })

class TestNoAudits(XSSParserTestBase):
    """
        Tests with no audits that empty lists are returned
    """
    def test(self):
        self._check_flagged_users(self.flags)

class TestAuditsNoFlags(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects but no audits. All ips are from the same country, no IPs are tor nodes.
        """
        post = self.create_post()
        
    def test(self):
        self._check_flagged_users(self.flags)

class TestAuditsURLFlag(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects and inject javascript into the url
        """
        post = self.create_post()

        for obj, xss in zip(post.audit_log.all(), TEST_XSS_INPUT):
            self.set_log_entry(obj, xss, "", "")
    
    def test(self):

        self.generic_t_est()

class TestAuditsGETFlag(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects and inject javascript into the get dict
        """
        post = self.create_post()

        for obj, xss in zip(post.audit_log.all(), TEST_XSS_INPUT):
            self.set_log_entry(obj, "", xss, "")

    def test(self):
        self.generic_t_est()

class TestAuditsPOSTFlag(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects and inject javascript into the post dict
        """
        post = self.create_post()

        for obj, xss in zip(post.audit_log.all(), TEST_XSS_INPUT):
            self.set_log_entry(obj, "", "", xss)

    def test(self):
        self.generic_t_est()

class TestAuditsAllFlags(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects and inject javascript into the url, get, and post dict
        """
        post = self.create_post()

        for obj, xss in zip(post.audit_log.all(), TEST_XSS_INPUT):
            self.set_log_entry(obj, xss, xss, xss)

    def test(self):
        self.generic_t_est()

class TestAuditsHexFlags(XSSParserTestBase):

    def generate_audits(self):
        """
            Generate audit objects and inject javascript into the url, get, and post dict
        """
        self.create_post()
        self.create_post()

        for obj, xss in zip(Post.audit_log.all(), TEST_XSS_INPUT):
            self.set_log_entry(obj, xss, xss, xss)

    def test(self):
        self.generic_t_est()
    
