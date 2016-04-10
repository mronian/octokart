from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Log(models.Model):
    ltype = models.CharField(max_length=300, null=False, blank=False)
    desc = models.TextField(null=False)
    timestamp = models.IntegerField(null=False, blank=False)
    
    def __unicode__(self):
        return self.ltype+":"+self.desc
