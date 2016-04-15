from __future__ import unicode_literals
from django.db import models

# Create your models here.

class SellerQueue(models.Model):
    
    seller_id=models.IntegerField(default=0)
    transaction_id=models.TextField()
    seq_id=models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.seller_id)+":"+self.transaction_id
    
class ItemQueue(models.Model):
    
    item_id=models.IntegerField(default=0)
    transaction_id=models.TextField()
    seq_id=models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.item_id)+":"+self.transaction_id

class SellerLock(models.Model):
    transaction_id=models.TextField();
    seller_id = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.item_id)+":"+self.transaction_id

class ItemLock(models.Model): 
    transaction_id=models.TextField();
    item_id = models.IntegerField(default=0)
    
    def __unicode__(self):
        return str(self.item_id)+":"+self.transaction_id

