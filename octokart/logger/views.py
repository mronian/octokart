from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from django.conf import settings 
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from ast import literal_eval

# Create your views here.
from .models import TransactionLog, CommitLog, LockLog, LoginLog, Message, getlogs, getlogsdict
from transactions.models import Connection

def locallogs(request):
    logs = getlogs()
    return render(request, 'logger/logs.html', {'logs' : logs})



@csrf_exempt
def alllogs(request):
    try:
        sender_port = request.POST['port']
        msg_id = request.POST['msg_id']
    except Exception:
        sender_port = None
        msg_id = str(Message.objects.count() + 1) + settings.SERVER_PORT

    try:
        message = Message.objects.get(msg_id = msg_id)
        return JsonResponse({})
    except Message.DoesNotExist:
        Message(msg_id = msg_id).save()
        params = urlencode({'port' : settings.SERVER_PORT, 'msg_id' : msg_id})
        my_data = getlogsdict()
        for connection in Connection.objects.all():
            if connection.port != sender_port:
                url = "http://%s:%s/logger/alllogs/" % (connection.ip, connection.port)
                response_data = urlopen(url, params).read()
                response_data = literal_eval(response_data)
                my_data.update(response_data)
        if sender_port is not None:
            return JsonResponse(my_data)
        else:
            logs = []
            for value in my_data.values():
                logs.append([value["timestamp"], value["describe"], value["site"]])
            logs = sorted(logs, key = lambda log: log[0], reverse = True)
            return render(request, 'logger/alllogs.html', {'logs': logs})



