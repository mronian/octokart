from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import TransactionLog, CommitLog, LockLog, LoginLog

def locallogs(request):
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
    return render(request, 'logger/logs.html', {'logs' : logs})
#    return render(request, 'logger/logs.html', {'logs' : [[1,"Hello"]]})
