from __future__ import unicode_literals

from django.db import models

# Create your models here.

class CatalogueItem(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    desc = models.TextField(null=False)
    upvotes = models.IntegerField(default=0)

    def __unicode__(self):
            return self.name
        
class UserItem(models.Model):
    
    pass