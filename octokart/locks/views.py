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
from threading import Thread, Lock
from seller.models import SellerItem
# Create your views here.

item_mutex=Lock()
seller_mutex=Lock()
# request for locking item table
@csrf_exempt
def items_request(request=None, msg=None, item_passed=None, curphase=1, curattempt=0, transaction_id=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        item=request.POST['item']
        phase=int(request.POST["phase"])
        attempt=int(request.POST["attempt"])
        transaction=request.POST["transaction"]
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE "+msg.mid+" ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" FOR ITEM "+str(item)
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        # self access of lock
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        item=item_passed
        phase=curphase
        attempt=curattempt
        transaction=transaction_id
        
    print "TRYING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item) +" IN PHASE "+str(phase)
    _,_,seq_id=transaction.split(":")
    
    if phase==1:
        try:
            item_queue_inst = ItemQueue.objects.get(transaction_id=transaction)
            print "TRANSACTION ALREADY QUEUED IN ITEMQUEUE AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" with transaction_id "+str(transaction_id)
        except ItemQueue.DoesNotExist:
            item_queue_inst=ItemQueue.objects.create(item_id=item,transaction_id=transaction, seq_id=int(seq_id));
            item_queue_inst.save()
            print item_queue_inst
    
    elif phase==2:
        for i in range(3):
            
            print "ATTEMPT "+str(i+1)+" TO GET SUBLOCK"
        
            t = Thread(target = grant_item_lock)
            t.start()
            t.join()
            lock=ItemLock.objects.all()[0]
            #if settings.SERVER_PORT=="5002" and attempt<2:
            #    lock=ItemLock.objects.create(transaction_id="FAILING", item_id=3)
            if lock.transaction_id==transaction:
                break
            
            if i==2:
                if attempt==2:
                    ItemQueue.objects.get(transaction_id=transaction).delete()
                print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item) +" IN PHASE "+str(phase)
                    
                return HttpResponse("Abort")
    
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, item=item, phase=phase, attempt=attempt, transaction=transaction)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/items/request/", encoded_params, msg, "TRYLOCK", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS ACQUIRED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item) +" IN PHASE "+str(phase)
        
        return HttpResponse("Success")
    else :
        
        release_item_lock()
        print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR ITEM "+str(item) +" IN PHASE "+str(phase)
        
        return HttpResponse("Abort")
            
# helper function for granting locks
def grant_item_lock():
    item_mutex.acquire()
    try:
        lock_status=ItemLock.objects.all()
        if len(lock_status)==0:
            item_to_be_locked=ItemQueue.objects.order_by('seq_id', 'transaction_id')
            if item_to_be_locked.exists():
                item_to_be_locked=item_to_be_locked[0]
                lock=ItemLock.objects.create(transaction_id=item_to_be_locked.transaction_id, item_id=item_to_be_locked.item_id)
                lock.save()
                item_to_be_locked.delete()
    finally:
        item_mutex.release()
# helper function for releasing locks
def release_item_lock():
    try:
        ItemLock.objects.all().delete()
    except:
        pass
    
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
    ItemLock.objects.all().delete()
    SellerItem.objects.all().delete()
    
    return redirect('/transactions/connections_manager/')
# when new seller is created seller 
@csrf_exempt
def seller_request(request=None, msg=None, seller_passed=None, curphase=1, curattempt=0, transaction_id=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        seller=request.POST['seller']
        phase=int(request.POST["phase"])
        attempt=int(request.POST["attempt"])
        transaction=request.POST["transaction"]
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE "+msg.mid+" ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" FOR ITEM "+str(seller)
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        seller=seller_passed
        phase=curphase
        attempt=curattempt
        transaction=transaction_id
        
    print "TRYING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller) +" IN PHASE "+str(phase)
    _,_,seq_id=transaction.split(":")
    
    if phase==1:
        try:
            seller_queue_inst = SellerQueue.objects.get(transaction_id=transaction)
            print "TRANSACTION ALREADY QUEUED IN SELLERQUEUE AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" with transaction_id "+str(transaction_id)
        except SellerQueue.DoesNotExist:
            seller_queue_inst=SellerQueue.objects.create(seller_id=seller,transaction_id=transaction, seq_id=int(seq_id));
            seller_queue_inst.save()
            print seller_queue_inst
    
    elif phase==2:
        for i in range(3):
            
            print "ATTEMPT "+str(i+1)+" TO GET SUBLOCK"
        
            t = Thread(target = grant_seller_lock)
            t.start()
            t.join()
            lock=SellerLock.objects.all()[0]
            #if settings.SERVER_PORT=="5002" and attempt<2:
            #    lock=SellerLock.objects.create(transaction_id="FAILING", seller_id=3)
            if lock.transaction_id==transaction:
                break
            
            if i==2:
                if attempt==2:
                    SellerQueue.objects.get(transaction_id=transaction).delete()
                print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller) +" IN PHASE "+str(phase)
                    
                return HttpResponse("Abort")
    
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, seller=seller, phase=phase, attempt=attempt, transaction=transaction)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/seller/request/", encoded_params, msg, "TRYLOCK", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS ACQUIRED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller) +" IN PHASE "+str(phase)
        
        return HttpResponse("Success")
    else :
        
        release_seller_lock()
        print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller) +" IN PHASE "+str(phase)
        
        return HttpResponse("Abort")
            
    
def grant_seller_lock():
    seller_mutex.acquire()
    try:
        lock_status=SellerLock.objects.all()
        if len(lock_status)==0:
            seller_to_be_locked=SellerQueue.objects.order_by('seq_id', 'transaction_id')
            if seller_to_be_locked.exists():
                seller_to_be_locked=seller_to_be_locked[0]
                lock=SellerLock.objects.create(transaction_id=seller_to_be_locked.transaction_id, seller_id=seller_to_be_locked.seller_id)
                lock.save()
                seller_to_be_locked.delete()
    finally:
        seller_mutex.release()
        
def release_seller_lock():
    try:
        SellerLock.objects.all().delete()
    except:
        pass
    
@csrf_exempt
def seller_release(request=None, msg=None, seller_passed=None):
    if request!=None:
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        seller=request.POST['seller']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport+" FOR SELLER "+str(seller)
            return HttpResponse("Seen")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        seller=seller_passed
        
    print "RELEASING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller)
    transaction=msg.mid
        
    release_seller_lock()

    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid, seller=seller)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/seller/release/", encoded_params, msg, "RELEASELOCK", reply)
    
    result=True
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS RELEASED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller)
        
        return HttpResponse("Success")
    else :
        print "RELEASELOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" FOR SELLER "+str(seller)
        
        return HttpResponse("Abort")


def seller_empty(request):
    SellerQueue.objects.all().delete()
    SellerLock.objects.all().delete()
    return redirect('/transactions/connections_manager/')
