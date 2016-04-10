from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.
class Connection(models.Model):
    
    ip = models.TextField(null=False, blank=False)
    port = models.TextField(null=False, blank=False)
    creator = models.TextField(default=settings.SERVER_ID_OCTOKART)
    
    def __unicode__(self):
            return self.ip+":"+self.port