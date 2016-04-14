from __future__ import unicode_literals

from django.db import models
from enum import Enum

class Operation(Enum):

    start = "START"
    ready = "READY"
    no = "NO"
    commit = "COMMIT"
    abort = "ABORT"
    lockrequest = "REQUEST LOCK"
    lockgrant = "GRANT LOCK"
    lockdeny = "DENY LOCK"
    lockrelease = "RELEASE LOCK"


# Create your models here.

class TransactionLog(models.Model):

    transaction_id = models.CharField(max_length = 50)
    seller_id = models.IntegerField()
    data_id = models.IntegerField()
    oldvalue = models.IntegerField()
    newvalue = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return "%d : <Transaction = %s, Seller = %d, Data = %d, Oldvalue = %d, Newvalue = %d>" % \
            (self.timestamp, self.transaction_id, self.seller_id, self.data_id, self.oldvalue, self.newvalue)

    def describe(self):
        return "Transaction %s updates quantity of data %d, sold by seller %d, from %d to %d" % \
                (self.transaction_id, self.data_id, self.seller_id, self.oldvalue, self.newvalue)

class CommitLog(models.Model):

    transaction_id = models.CharField(max_length = 50)
    timestamp = models.IntegerField()
    operation = models.CharField(max_length = 50)

    def __str__(self):
        return "%d : <Transaction = %s, operation = %s>" % (self.timestamp, self.transaction_id,
            self.operation)

    def describe(self):
        return "Commit Log"

class LockLog(models.Model):

#   mode = True means Receive a request, mode = False means send a request
    transaction_id = models.CharField(max_length = 50)
    site_id = models.CharField(max_length = 50)
    mode = models.BooleanField(default = False)
    operation = models.CharField(max_length = 50)
    timestamp = models.IntegerField()

    def __str__(self):
        if self.mode == True:
            return "%d : <Transaction = %s, RECEIVING %s FROM %s>" % (self.timestamp, self.transaction_id,
                    self.operation, self.site_id)
        else:
            return "%d : <Transaction = %s, SENDING %s TO %s>" % (self.timestamp, self.transaction_id,
                    self.operation, self.site_id)

    def describe(self):
        return "Lock Log"

class LoginLog(models.Model):

#    mode = True means login, mode = False means logout
    seller_id = models.IntegerField()
    mode = models.BooleanField(default = True)
    timestamp = models.IntegerField()

    def __str__(self):
        if self.mode == True:
            return "%d : <Seller %d HAS LOGGED IN>" % (self.timestamp, self.seller_id)
        else:
            return "%d : <Seller %d HAS LOGGED OUT>" % (self.timestamp, self.seller_id)

    def describe(self):
        return "Login Log"

