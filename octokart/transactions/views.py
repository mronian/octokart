from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import Connection
from django.conf import settings
import socket
import urllib2
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from django.views.decorators.csrf import csrf_exempt
socket.setdefaulttimeout( 23 )  # timeout in seconds

@csrf_exempt
def receive_connection(request):
    new_ip=request.POST["ip"]
    new_port=request.POST['port']
    conn, _=Connection.objects.get_or_create(ip=new_ip, port=new_port)
    
    return HttpResponse("Connection Added")

# Create your views here.
def add_connection(request):
    new_ip=request.POST["ip"]
    new_port=request.POST['port']
    conn, _=Connection.objects.get_or_create(ip=new_ip, port=new_port)
    post_data=[('ip',conn.ip), ('port',conn.port)]
    url="http://"+conn.ip+":"+conn.port+"/transactions/connections_manager/receive_connection/"
   
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT)
    encoded_params = urlencode(params)
    response=urlopen(url, encoded_params)
    return redirect('/transactions/connections_manager/')

def delete_connections(request):
    Connection.objects.all().delete()
    
    return redirect('/transactions/connections_manager/')

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
    
    active_connections=Connection.objects.all()
    
    return render(request, 'transactions/manager.html', {'connections':active_connections})
    

