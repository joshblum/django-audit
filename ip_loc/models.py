from django.db import models

from ip_loc.helpers import std_to_decimal_ip as parse_ip

from datetime import datetime

class IPtoLoc(models.Model):
    ip_to = models.CharField(max_length=15)
    ip_fr = models.CharField(max_length=15)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=200)

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return "%s | %s : %s" %(self.ip_to, self.ip_fr, self.country_name)

class TorNode(models.Model):
    ip = models.CharField(max_length=15)

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return "%s is a tor node" %(self.ip)