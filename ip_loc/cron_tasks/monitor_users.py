from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from ip_loc.models import *
from ip_loc.helpers import std_to_decimal_ip as parse_ip
from ip_loc.query_managers import *

import urllib

class MonitorUsers():
    """
        Search AuditLogs and build users that might have been compromised.
    """

    def run(self):
        flagged_countries, flagged_tor = self.check_audit_objects()

        flagged_users = {
            'flagged_tor' : flagged_tor,
            'flagged_countries' : flagged_countries
        }
        self.email_admin(flagged_users)

    def check_audit_objects(self):
        """
            Finds all of the models that are AuditLogs.
            Deletes objects that have noneType users and returns the rest.
            noneType users are a result of object creation and django internals.
        """
        flagged_countries = []
        flagged_tor = []

        for model in models.get_models():
            if self._check_name(model):
                country_flags, tor_flags = self.check_users(model.objects.all())
                flagged_countries.extend(country_flags)
                flagged_tor.extend(tor_flags)

        return flagged_countries, flagged_tor

                
    def _check_name(self, cls):
        return "AuditLogEntry" in cls.__name__    

    def check_users(self, objs):
        """
            Iterates over objects and determines if the country has changed from previous log ons or if the user is using a TOR node.
        """
        objs = self._clean_objects(objs)
        
        user_map = self._get_user_map(objs)

        country_flags = []
        tor_flags = []
        for username, obj_list in user_map.items():
            c_codes = {}
            tor_nodes = []
            for obj in obj_list:
                ip = obj.action_ip
                obj.is_new = False
                obj.save()

                #convert to country code
                code = ip_to_ccode(ip) 
                if c_codes.get(code):
                    c_codes[code].append(ip)
                else:
                    c_codes[code] = [ip]

                #check if a tor node
                if check_tor(ip):
                    tor_nodes.append(ip)

            if len(c_codes) > 1:
                country_flags.append({username : c_codes})

            if len(tor_nodes):
                tor_flags.append({username : tor_nodes})

        return country_flags, tor_flags
        
    def _get_user_map(self, objs):
        """
            Returns a hashmap of usernames to objects to be checked
        """
        seen_users = {} #lets hash the users we've seen so far

        for obj in objs:
            user = obj.action_user
            if seen_users.get(user.username):
                pass
            else:
                seen_users[user.username] = objs.filter(action_user=user)
        return seen_users

    def _clean_objects(self, objs):
        """ 
            Objects that have no user or empty IP fields are removed
        """
        objs.filter(action_ip=None).delete()

        return objs.filter(is_new=True)

    def email_admin(self, flagged_users):
        """
            Takes a dictionary of flagged users. Dictionary maps flag type to user set.
        """
        admin_emails = self._get_admins(settings.ADMINS)
        from_email = "audit-service@example.com"

        for flag_type, users in flagged_users.items():
            if len(users):
                template_values = {
                    'flag_type' : flag_type,
                    'users' : users,
                }
                subject = "Django-Audit alert: %s Flag" % flag_type

                msg = render_to_string('ip_loc/email_template.txt',template_values)
                send_mail(subject, msg, from_email, admin_emails, fail_silently=False)

    def _get_admins(self, admins):
        return [email for name, email in admins]