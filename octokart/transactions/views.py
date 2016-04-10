from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import Connection
from django.conf import settings
import socket
from urllib2 import urlopen, URLError, HTTPError

socket.setdefaulttimeout( 23 )  # timeout in seconds


# Create your views here.
def add_connection(request):
    new_ip=request.POST["ip"]
    new_port=request.POST['port']
    Connection.objects.get_or_create(ip=new_ip, port=new_port)
    
    return redirect('/transactions/connections_manager/')

def delete_connections(request):
    Connection.objects.filter(creator=settings.SERVER_ID_OCTOKART).delete()
    
    return redirect('/transactions/connections_manager/')

def check_connection(request):
    conns=Connection.objects.all()
    for c in conns:
        print c.id
    conn_id=request.GET[u'id']
    print conn_id
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
    
    active_connections=Connection.objects.filter(creator=settings.SERVER_ID_OCTOKART)
    
    for conn in active_connections:
        print conn.creator
    
    
    return render(request, 'transactions/manager.html', {'connections':active_connections})
    

