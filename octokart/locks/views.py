from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import SellerQueue, ItemQueue, SellerLock, ItemLock
from transactions.flood import flood
from django.conf import settings
import urllib2
from transactions.models import Message
from urllib2 import urlopen, URLError, HTTPError
from urllib import urlencode
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def seller_request(request):
    seller_id=request.POST['seller_id']
    transaction_id=request.POST['transaction_id']
    try:
        seller_queue_item = SellerQueue.objects.get(transaction_id=transaction_id)
        print "Transaction Already queued at "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" with transaction_id "+str(transaction_id)
        #what should we do?
    except SellerQueue.DoesNotExist:
        seller_queue_item=Message.objects.create(transaction_id=transaction_id,seller_id=seller_id);
        seller_queue_item.save()
    msg = Message.objects.get(mid=msg_id)
    pass

def seller_release(request):
    pass

@csrf_exempt
def items_request(request=None, msg=None, item_passed=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        item=request.POST['item']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" FOR ITEM "+str(item)
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        item=item_passed
        
    print "TRYING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
    transaction=msg.mid
    
    try:
        item_queue_inst = ItemQueue.objects.get(transaction_id=transaction)
        print "TRANSACTION ALREADY QUEUED IN ITEMQUEUE AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" with transaction_id "+str(transaction_id)
    except ItemQueue.DoesNotExist:
        item_queue_inst=ItemQueue.objects.create(item_id=item,transaction_id=transaction);
        item_queue_inst.save()
        
    grant_item_lock()
        
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, item=item)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/items/request/", encoded_params, msg, "TRYLOCK", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS ACQUIRED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
        
        return HttpResponse("Success")
    else :
        print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
        
        return HttpResponse("Abort")

def grant_item_lock():
    lock_status=ItemLock.objects.all()
    
    if not lock_status:
        print ItemQueue.objects.order_by('id')
        item_to_be_locked=ItemQueue.objects.order_by('id')[0]
        lock=ItemLock.objects.create(transaction_id=item_to_be_locked.transaction_id, item_id=item_to_be_locked.item_id)
        lock.save()
        item_to_be_locked.delete()
        print lock
        
def release_item_lock():
    ItemLock.objects.all().delete()
    item_to_be_locked=ItemQueue.objects.order_by('id')[0]
    lock=ItemLock.objects.create(transaction_id=item_to_be_locked.transaction_id, item_id=item_to_be_locked.item_id)
    lock.save()
    item_to_be_locked.delete()
    
@csrf_exempt
def items_release(request=None, msg=None, item_passed=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        item=request.POST['item']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" FOR ITEM "+str(item)
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        item=item_passed
        
    print "RELEASING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
    transaction=msg.mid
        
    release_item_lock()

    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, item=item)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/items/release/", encoded_params, msg, "RELEASELOCK", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS RELEASED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
        
        return HttpResponse("Success")
    else :
        print "RELEASELOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item)
        
        return HttpResponse("Abort")

def items_empty(request):
    ItemQueue.objects.all().delete()
    return redirect('/transactions/connections_manager/')

def seller_empty(request):
    SellerQueue.objects.all().delete()
    return redirect('/transactions/connections_manager/')