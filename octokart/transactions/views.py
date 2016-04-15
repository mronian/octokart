from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import Connection, Message
from django.conf import settings
import socket
import urllib2
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from django.views.decorators.csrf import csrf_exempt
from locks.views import items_request, items_release
from flood import flood
import time

socket.setdefaulttimeout( 23 )  # timeout in seconds

transaction_type=['seller', 'items']

@csrf_exempt
def receive_connection(request):
    new_ip=request.POST["ip"]
    new_port=request.POST['port']
    conn, _=Connection.objects.get_or_create(ip=new_ip, port=new_port)
    
    return HttpResponse("Connection Added")

@csrf_exempt
def prepare_for_commit(request=None, msg=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE "+str(msg)+" ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        
    print "PREPARING FOR PRECOMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
    
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/transactions/prepare/", encoded_params, msg, "PRECOMMIT", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "READY FOR PRECOMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Success")
    else :
        print "PRECOMMIT ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Abort")

@csrf_exempt
def commit(request=None, msg=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE "+str(msg)+" ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        
    print "PREPARING FOR COMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
    
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/transactions/prepare/", encoded_params, msg, "COMMIT", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "READY FOR COMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Success")
    else :
        print "COMMIT ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Abort")
    
    
def release_locks(msg, table_to_lock):
    print "RELEASING LOCKS FOR TABLE:"+table_to_lock
    
    if table_to_lock=="items":
        response=items_release(None, msg, 1)
    
    print "RELEASED LOCKS FROM ALL CONNECTIONS FOR TABLE:"+table_to_lock
    
    return "Success"


def acquire_locks(msg, table_to_lock):
    
    print "REQUESTING LOCKS FOR TABLE:"+table_to_lock
    
    for i in range(3):
        
        print "ATTEMPT "+str(i+1)+" TO GET LOCKS FROM COORDINATOR"
        if table_to_lock=="items":
            response=items_request(None, msg, 1, 1, i, msg.mid)
        
        if response.getvalue()=="Success":
            
                msg2=create_message()
                response=items_request(None, msg2, 1, 2, i, msg.mid)
                
                if response.getvalue()=="Success":
                    
                    print "ACQUIRED LOCKS FROM ALL CONNECTIONS FOR TABLE:"+table_to_lock
                
                    return "Success"
                
                time.sleep(0.5)
            
    print "LOCKS COULD NOT BE ACQUIRED"
    
    return "Abort"
    
@csrf_exempt
def perform_transaction(request):
    
    trans_type_id=1
    #trans_type=int(request.POST["trans_type"])
    table_to_lock=transaction_type[trans_type_id]
    
    msg=create_message()
    
    locked=acquire_locks(msg, table_to_lock)
    if locked=="Success":
        msg=create_message()
        response=prepare_for_commit(None, msg)
        response=HttpResponse("Success")  
        
        if response.getvalue()=="Success":
            response=commit(None, msg)
        
            msg=create_message()    
            release_locks(msg, table_to_lock)
    
            if response.getvalue()=="Success":
                return HttpResponse("Success")
        
    return HttpResponse("Abort")

def create_message():
    msg=Message.objects.create()
    msg.mid=settings.SERVER_ID_OCTOKART+":"+str(msg.id)    
    msg.save()
    return msg

# Create your views here.
def add_connection(request):
    new_ip=request.POST["ip"]
    new_port=request.POST['port']
    conn, _=Connection.objects.get_or_create(ip=new_ip, port=new_port)
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
    

