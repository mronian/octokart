from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from models import Connection
import socket
from urllib2 import urlopen, URLError, HTTPError

socket.setdefaulttimeout( 23 )  # timeout in seconds


# Create your views here.
def make_connection():
    pass

def check_connections(request):
    url = 'http://google.com/'
    try :
        response = urlopen( url )
    except HTTPError, e:
        print 'The server couldn\'t fulfill the request. Reason:', str(e.code)
    except URLError, e:
        print 'We failed to reach a server. Reason:', str(e.reason)
    else :
        html = response.read()
        print 'got response!'
    return JsonResponse({"success":"success"})

def close_connection():
    pass

def connections_manager(request):
    
    Connection.objects.get_or_create(ip="127.0.0.1", port="8000")
    Connection.objects.get_or_create(ip="127.0.0.2", port="8010")
    
    active_connections=Connection.objects.all()
    
    return render(request, 'transactions/manager.html', {'connections':active_connections})
    

