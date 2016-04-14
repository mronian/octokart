from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.
class Connection(models.Model):
    
    ip = models.TextField(null=False, blank=False)
    port = models.TextField(null=False, blank=False)
    
    def __unicode__(self):
            return self.ip+":"+self.port
        

class Message(models.Model):
    
    mid=models.TextField()
    
    def __unicode__(self):
            return self.mid        
