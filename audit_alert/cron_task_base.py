from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

from audit_log.admin import _check_name

from audit_alert.models import FlaggedUser

from datetime import datetime, timedelta

DAYS = 2
ADMINS = settings.ADMINS
EMAIL_ADMIN = getattr(settings, 'LOC_EMAIL_ADMIN', True)
FROM_EMAIL = getattr(settings, 'LOC_FROM_EMAIL', "audit-service@example.com")

class CronBase():
    """
        Base class to extend when creating cron jobs using django-audit-log
    """

    def __init__(self, flags):
        self.flagged_users = dict([(flag, []) for flag in flags])

    def run(self):

        self.flagged_users = self.check_audit_objects(self.flagged_users)
        
        self.flag_users(self.flagged_users)

    def check_audit_objects(self, flag_dict):
        """
            Finds all of the models that are AuditLogs and flags the users that are potentially compromised. 
            Takes a flag_dict as input in the form:

            {
                FLAG_TYPE : []
            }

            and returns a modified dictionary with the flagged items for each type.
        """

        for model in models.get_models():
            if _check_name(model):
                
                flags = self.check_users(model.objects.all())
                
                for key, value in flag_dict.items():
                    value.extend(flags[key])
                    flag_dict[key] =  value

        return flag_dict

    def check_users(self, objs):
        """
            Required method of subclasses
        """
        raise NotImplementedError("Abstract function must be implemented")

    def _get_user_map(self, objs):
        """
            Returns a hashmap of usernames to audit_log_objects to be checked
        """
        seen_users = {} #lets hash the users we've seen so far

        for obj in objs:
            user = obj.action_user
            if not seen_users.get(user.username):
                seen_users[user.username] = objs.filter(action_user=user)
        return seen_users

    def _clean_objects(self, objs):
        """ 
            Objects that have no user or empty IP fields are removed
        """
        objs.filter(action_ip=None).delete()

        date = datetime.today() - timedelta(days=DAYS)
        
        objs.filter(action_date__lt=date)
        
        return objs

    def flag_users(self, flagged_users):
        """
            Adds flagged users to the database.
            Flagged_users is a dictionary:

            {
                flag_types: [{flagged_user:data}]
            }
        """

        for flag_type, users in flagged_users.items():
            for user in users:
                try:
                    username =  user.keys()[0]
                    data = user[username]
                    user = User.objects.get(username=username)
                    
                    user = FlaggedUser(user=user, flag_type=flag_type, data=data)
                    user.save()
                
                except Exception as e:
                    print str(e)

        if EMAIL_ADMIN:
            self.email_admin(flagged_users.keys())
    
    def email_admin(self, flag_types):
        """
            Takes a dictionary of flagged users. Dictionary maps flag type to user set.
        """

        for flag_type in flag_types:
            flagged_users = FlaggedUser.objects.filter(flag_type=flag_type, is_new=True, flagged=True)
       
            if flagged_users.exists():
                self._email_admin_util(flag_type, flagged_users)
                self._update_objs(flagged_users)

    def _update_objs(self, objs):
        for obj in objs:
            obj.is_new = False
            obj.save()

    def _email_admin_util(self, flag_type, objs):
        admin_emails = self._get_admins(ADMINS)

        template_values = {
            'flag_type' : flag_type,
            'users' : objs,
        }
        subject = "Django-Audit alert: %s Flag" % flag_type

        msg = render_to_string('audit_alert/email_template.txt',template_values)
        send_mail(subject, msg, FROM_EMAIL, admin_emails, fail_silently=False)

    def _get_admins(self, admins):
        return [email for name, email in admins]