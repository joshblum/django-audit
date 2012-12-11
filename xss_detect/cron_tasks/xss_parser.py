from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from audit_alert.cron_task_base import CronBase

from audit_log.admin import _check_name

from datetime import datetime, timedelta

XSS_FLAG = 'flagged_xss'
FLAG_STRINGS = ['<script>', '<style>', 'type=text/javscript', '</script>', '</style>']

class XSSParser(CronBase):
    """
        Parses audit log entries to use best effort detection the use of javascript in the request url, GET, and POST params.
    """

    def check_users(self, objs):
        """
            Iterates over objects and determines an injection was placed in either the request_url, GET params, or POST params. 
        """
        objs = self._clean_objects(objs)
        
        user_map = self._get_user_map(objs)

        xss_flags = []
        for username, obj_list in user_map.items():
            flags = []
            for obj in obj_list:
                url = obj.action_request_url
                get = obj.action_post_params,
                post = obj.action_post_params
                for item in [url, get, post]:
                    if self._check_string(item):
                        flags.append(item)

            if len(flags):
                xss_flags.append({username : flags})

        return {
            XSS_FLAG : xss_flags
        }

    def _check_string(self, string):
        string = str(string)
        flagged = False
        for item in FLAG_STRINGS:
            if item in string:
                flagged = True
                break
        return flagged
