from django.db import models
from django.contrib.auth.models import User
from django.utils import simplejson as json

from datetime import datetime

# Create your models here.
class FlaggedUser(models.Model):
    user = models.ForeignKey(User, related_name='flagged_user')
    flag_type = models.CharField(max_length=40) 
    data = models.TextField()
    
    is_new = models.BooleanField(default=True)
    flagged = models.BooleanField(default=True) #admin can clear the flag if necessary

    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def save(self, *args, **kwargs):
        self.data = json.dumps(self.data)
        super(FlaggedUser, self).save(*args, **kwargs)


    def __unicode__(self):
        return "Flagged user %s | flagged: %s | %s" % (self.user.username, self.flagged, json.loads(self.data))