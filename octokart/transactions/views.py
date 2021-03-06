from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import Connection, Message
from django.conf import settings
import socket
import urllib2
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from django.views.decorators.csrf import csrf_exempt
from locks.views import items_request, items_release, seller_request, seller_release
from seller.models import SellerItem, CatalogueItem
from logger.models import Operation
from logger.models import writetransactionlog, writecommitlog, writelocklog, writeloginlog
from logger.models import getTime, updateTime
from django.contrib.auth.models import User
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
def prepare_for_commit(request=None, msg=None, item=None, seller=None):
    print "ENTERED PRECOMMIT"

    t_type=None
    item_iid=None
    item_sid=None
    item_q=None
    seller_uid=None
    seller_pwd=None
    flag = 0

    if request!=None:
        
        msg_id=request.POST['message']
        mip=request.POST['ip']
        mport=request.POST['port']
        t_type=request.POST[u'trans_type']
        timestamp=request.POST['timestamp']
        updateTime(timestamp)
        
        if t_type=="items":
            item_iid=request.POST['item_item_id']
            item_sid=request.POST['item_seller_id']
            item_q=int(request.POST['item_quantity'])
            try:
                item = SellerItem.objects.get(item_id=CatalogueItem.objects.get(name=item_iid), seller_id=User.objects.get(username=item_sid))
                flag = 1
            except SellerItem.DoesNotExist:
                flag=0
                item=SellerItem(item_id=CatalogueItem.objects.get(name=item_iid), seller_id=User.objects.get(username=item_sid), quantity=item_q)
        
        
        elif t_type=="seller":
            seller_uid=request.POST['seller_uid']
            seller_pwd=request.POST['seller_pwd']
            try:
                seller = User.objects.get(username=seller_uid)
            except User.DoesNotExist:
                
                seller = User(username=seller_uid)
                seller.set_password(seller_pwd)
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
        
        if item!=None:
            t_type="items"
            item_iid=item.item_id.name
            item_sid=item.seller_id.username
            item_q=item.quantity
            
        else:
            t_type="seller"
            seller_uid = seller['username']
            seller_pwd = seller['password']
            seller=User(username=seller_uid)
            seller.set_password(seller_pwd)
        
        try:
                test_item = SellerItem.objects.get(item_id=item.item_id, seller_id=item.seller_id)
                flag = 1
                item=test_item
        except SellerItem.DoesNotExist:
            flag=0
    writecommitlog(transaction_id = msg.mid, operation = Operation.start)
    print "PREPARING FOR PRECOMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
    params=None
    if t_type=="items":
        params = dict(timestamp = getTime(), ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, trans_type=t_type, item_item_id=item_iid, item_seller_id=item_sid, item_quantity=item_q)
    elif t_type=="seller":
        params = dict(timestamp = getTime(), ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, trans_type=t_type, seller_uid=seller_uid, seller_pwd=seller_pwd)

    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/transactions/prepare/", encoded_params, msg, "PRECOMMIT", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        if t_type=='items':
            writecommitlog(transaction_id = msg.mid, operation = Operation.ready)
            writetransactionlog(transaction_id = msg.mid, seller_id = item_sid, data_id = item_iid, oldvalue = 0, newvalue = item.quantity)
        
            if flag==0:
                item.save()
            else:
                item.quantity-=item_q
                item.save()
                
        elif t_type=='seller':
            seller.save()
            
        print "READY FOR PRECOMMIT AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Success")
    else :
        writecommitlog(transaction_id = msg.mid, operation = Operation.no)
        print "PRECOMMIT ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Abort")

@csrf_exempt
def commit(request=None, msg=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        timestamp=request.POST['timestamp']
        updateTime(timestamp)
                
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
    
    params = dict(timestamp = getTime(), ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/transactions/commit/", encoded_params, msg, "COMMIT", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "COMMITTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        writecommitlog(transaction_id = msg.mid, operation = Operation.commit)
        return HttpResponse("Success")
    else :
        print "COMMIT ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        writecommitlog(transaction_id = msg.mid, operation = Operation.abort)
        return HttpResponse("Abort")
    
    
def release_locks(msg, table_to_lock):
    print "RELEASING LOCKS FOR TABLE:"+table_to_lock
    
    if table_to_lock=="items":
        response=items_release(None, msg, 1)
    elif table_to_lock=="seller":
        response=seller_release(None, msg, 1)
    
    print "RELEASED LOCKS FROM ALL CONNECTIONS FOR TABLE:"+table_to_lock
    
    return "Success"


def acquire_locks(msg, table_to_lock, field):
    
    print "REQUESTING LOCKS FOR TABLE:"+table_to_lock
    response=None
    print field
    print field.item_id
    print field.item_id.name
    
    for i in range(3):
        
        print "ATTEMPT "+str(i+1)+" TO GET LOCKS FROM COORDINATOR"
        if table_to_lock=="items":
            response=items_request(None, msg, field.item_id.name, 1, i, msg.mid)
            
        elif table_to_lock=="seller":
            response=seller_request(None, msg, field['username'], 1, i, msg.mid)
        
        if response.getvalue()=="Success":
            
            msg2=create_message()
            
            if table_to_lock=="items":
                response=items_request(None, msg2, field.item_id.name, 2, i, msg.mid)
            elif table_to_lock=="seller":
                response=seller_request(None, msg2, field['username'], 2, i, msg.mid)
                
            if response.getvalue()=="Success":
                
                print "ACQUIRED LOCKS FROM ALL CONNECTIONS FOR TABLE:"+table_to_lock
            
                return "Success"
            
            #time.sleep(0.5)
            
    print "LOCKS COULD NOT BE ACQUIRED"
    
    return "Abort"
    
@csrf_exempt
def perform_transaction(request=None, seller=None, item=None):
    if item!=None:
        trans_type_id=1
    else:
        trans_type_id=0
    #item=SellerItem(item_id=CatalogueItem.objects.get(id=1), seller_id=User.objects.get(id=1), quantity=50)
    #trans_type_id=1
    #trans_type=int(request.POST["trans_type"])
    table_to_lock=transaction_type[trans_type_id]
    
    msg=create_message()
    locked=None
    if trans_type_id==1:
        locked=acquire_locks(msg, table_to_lock, item)
    else :
        locked=acquire_locks(msg, table_to_lock, seller)
    
    response=None
    if locked=="Success":
        msg=create_message()
        
        if trans_type_id==1:    
            response=prepare_for_commit(None, msg, item, None)
        else :
            response=prepare_for_commit(None, msg, None, seller)
        
        if response.getvalue()=="Success":
            msg=create_message()
                    
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
    

