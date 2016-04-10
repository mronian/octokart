from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from models import Connection
import socket
from urllib2 import urlopen, URLError, HTTPError

socket.setdefaulttimeout( 23 )  # timeout in seconds


# Create your views here.
def make_connection():
    pass

def check_connection(request):
    conn_id=request.GET[u'id']
    conn=Connection.objects.get(id=conn_id)
    url="http://"+conn.ip+":"+conn.port+"/transactions/connections_manager/"
    result=""
    try :
        response = urlopen( url )
    except HTTPError, e:
        result = 'The server couldn\'t fulfill the request. Reason:'+str(e.code)
    except URLError, e:
        result =  'We failed to reach a server. Reason:'+str(e.reason)
    else :
        html = response.read()
        result = 'Works'
    return JsonResponse({"success":result})

def close_connection():
    pass

def connections_manager(request):
    
    Connection.objects.get_or_create(ip="10.109.9.63", port="4000")
    Connection.objects.get_or_create(ip="10.109.9.63", port="5000")
    Connection.objects.get_or_create(ip="10.109.9.63", port="6000")
    
    active_connections=Connection.objects.all()
    
    return render(request, 'transactions/manager.html', {'connections':active_connections})
    

