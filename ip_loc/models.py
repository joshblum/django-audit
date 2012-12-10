from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json

from ip_loc.helpers import std_to_decimal_ip as parse_ip

from datetime import datetime

class IPtoLoc(models.Model):
    ip_to = models.IntegerField(max_length=15)
    ip_fr = models.IntegerField(max_length=15)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=200)

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return "%s | %s : %s" %(self.ip_to, self.ip_fr, self.country_name)

class TorNode(models.Model):
    ip = models.IntegerField(max_length=15)

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return "%s is a tor node" %(self.ip)

class FlaggedUser(models.Model):
    user = models.ForeignKey(User, related_name='flagged_user')
    flag_type = models.CharField(max_length=40) #tor flag or country flag
    data = models.TextField()
    
    is_new = models.BooleanField(default=True)
    flagged = models.BooleanField(default=True) #admin can clear the flag if necessary

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def save(self, *args, **kwargs):
        self.data = json.dumps(self.data)
        super(FlaggedUser, self).save(*args, **kwargs)


    def __unicode__(self):
        return "Flagged user %s | flagged: %s | %s" % (self.user.username, self.flagged, json.loads(self.data))
