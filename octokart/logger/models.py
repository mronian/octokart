from __future__ import unicode_literals

from django.db import models
from django.db.models import F
from django.conf import settings
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
    seller_id = models.CharField(max_length = 50)
    data_id = models.CharField(max_length = 50)
    oldvalue = models.IntegerField()
    newvalue = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return "%d : <Transaction = %s, Seller = %s, Data = %s, Oldvalue = %d, Newvalue = %d>" % \
            (self.timestamp, self.transaction_id, self.seller_id, self.data_id, self.oldvalue, self.newvalue)

    def describe(self):
        return "Transaction %s updates quantity of data %s, sold by seller %s, from %d to %d" % \
                (self.transaction_id, self.data_id, self.seller_id, self.oldvalue, self.newvalue)

class CommitLog(models.Model):

    transaction_id = models.CharField(max_length = 50)
    timestamp = models.IntegerField()
    operation = models.CharField(max_length = 50)

    def __str__(self):
        return "%d : <Transaction = %s, operation = %s>" % (self.timestamp, self.transaction_id,
            self.operation)

    def describe(self):
        return "Transaction %s : %s" % (self.transaction_id, self.operation)

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
        if self.mode == False:
            if self.operation == Operation.lockrequest:
                return "Sent lock request for transaction %s to site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockgrant:
                return "Granted lock request for transaction %s to site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockdeny:
                return "Denied lock request for transaction %s to site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockrelease:
                return "Released lock for transaction %s on site %s" % (self.transaction_id, 
                    self.site_id)
        else:
            if self.operation == Operation.lockrequest:
                return "Received lock request for transaction %s from site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockgrant:
                return "Granted lock request for transaction %s from site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockdeny:
                return "Denied lock request for transaction %s from site %s" % (self.transaction_id, 
                    self.site_id)
            elif self.operation == Operation.lockrelease:
                return "Released lock for transaction %s by site %s" % (self.transaction_id, 
                    self.site_id)

class LoginLog(models.Model):

#    mode = True means login, mode = False means logout
    seller_id = models.CharField(max_length = 50)
    mode = models.BooleanField(default = True)
    timestamp = models.IntegerField()

    def __str__(self):
        if self.mode == True:
            return "%d : <Seller %s HAS LOGGED IN>" % (self.timestamp, self.seller_id)
        else:
            return "%d : <Seller %s HAS LOGGED OUT>" % (self.timestamp, self.seller_id)

    def describe(self):
        if self.mode == True:
            return "Seller %s has logged in" % self.seller_id
        else:
            return "Seller %s has logged out" % self.seller_id

class Message(models.Model):

    msg_id = models.CharField(max_length = 50)

    def __str__(self):
        return "Msg Id = %s" % (self.msg_id)

class Timestamp(models.Model):

    timestamp = models.IntegerField(default = 0)

    def __str__(self):
        return "timestamp = %d" % self.timestamp

def resetTime():
    Timestamp.objects.all().delete()

def getTime():
    if Timestamp.objects.count() == 0:
        t = Timestamp(timestamp = 1)
        t.save()
    else:
        t = Timestamp.objects.all()[0]
        t.timestamp += 1
        t.save()
    return t.timestamp

def updateTime(timestamp):
    if Timestamp.objects.count() == 0:
        t = Timestamp(timestamp = timestamp)
        t.save()
    else:
        t = Timestamp.objects.all()[0]
        t.timestamp = max(t.timestamp, timestamp)
        t.save()

def getlogs():
    rawtransactionlogs = TransactionLog.objects.all()
    rawcommitlogs = CommitLog.objects.all()
    rawlocklogs = LockLog.objects.all()
    rawloginlogs = LoginLog.objects.all()

    logs = [[rawtransactionlog.timestamp, rawtransactionlog.describe()] \
                       for rawtransactionlog in rawtransactionlogs]
    logs.extend([[rawcommitlog.timestamp, rawcommitlog.describe()] \
                           for rawcommitlog in rawcommitlogs])
    logs.extend([[rawlocklog.timestamp, rawlocklog.describe()] \
                   for rawlocklog in rawlocklogs])
    logs.extend([[rawloginlog.timestamp, rawloginlog.describe()] \
                       for rawloginlog in rawloginlogs])
                       
    logs = sorted(logs, key = lambda log: log[0], reverse = True)
    return logs

def getlogsdict():
    logs = getlogs()
    data = {}
    i = 1
    for log in logs:
        data[str(i) + settings.SERVER_PORT] = \
        {"timestamp" : log[0], "describe" : log[1], \
        "site" : settings.SERVER_IP + ":" + settings.SERVER_PORT}
        i += 1
    return data

def clearalllogs():
    TransactionLog.objects.all().delete()
    CommitLog.objects.all().delete()
    LockLog.objects.all().delete()
    LoginLog.objects.all().delete()

def writetransactionlog(transaction_id, seller_id ,data_id, oldvalue, newvalue):
    log = TransactionLog(transaction_id = transaction_id, data_id = data_id, seller_id = seller_id,
        oldvalue = oldvalue, newvalue = newvalue, timestamp = getTime())
    log.save()

def writecommitlog(transaction_id, operation):
    log = CommitLog(transaction_id = transaction_id, operation = operation, timestamp = getTime())
    log.save()

def writelocklog(transaction_id, operation, site_id, mode):
    log = LockLog(transaction_id = transaction_id, operation = operation, site_id = site_id, 
        mode = mode, timestamp = getTime())
    log.save()

def writeloginlog(seller_id, mode):
    log = LoginLog(seller_id = seller_id, mode = mode)
    log.save()




