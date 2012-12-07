from django.db import models

class IPtoLoc(models.Model):
    ip_to = models.CharField(max_length=15)
    ip_fr = models.CharField(max_length=15)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s | %s : %s" %(ip_to, ip_fr, country_name)

class TorNode(models.Model):
    ip = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s is a tor node" %(ip)