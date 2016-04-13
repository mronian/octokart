from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class CatalogueItem(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    desc = models.TextField(null=False)
    upvotes = models.IntegerField(default=0)

    def __unicode__(self):
            return self.name
        
class SellerItem(models.Model):
    item_id=models.ForeignKey(CatalogueItem)
    seller_id=models.ForeignKey(User)
    quantity = models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.seller_id)+":"+str(self.item_id)+":"+str(self.quantity)