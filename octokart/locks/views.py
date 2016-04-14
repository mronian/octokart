from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from models import SellerQueue, ItemQueue
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
def items_request(request="self", msg="default"):
    if request!="self":
        msg_id=request.POST["message"]
        mip=request.POST["ip"]
        mport=request.POST['port']
        
        try:
            msg = Message.objects.get(mid=msg_id)
            print "MESSAGE ALREADY SEEN AT "+settings.SERVER_IP+":"+settings.SERVER_PORT+" SENT BY "+mip+":"+mport
            return HttpResponse("Success")
        except Message.DoesNotExist:
            msg=Message.objects.create(mid=msg_id)  
            msg.save() 
       
    else :
        mip=settings.SERVER_IP
        mport=settings.SERVER_PORT
        
    print "TRYING LOCK AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
    
    params = dict(ip=settings.SERVER_IP, port=settings.SERVER_PORT, message=msg.mid)
    encoded_params = urlencode(params)
    reply={}
    reply=flood(mip, mport, "/locks/items/request/", encoded_params, msg, "TRYLOCK", reply)
    
    result=True
    print reply
    for v in reply.values():
        if v=="Abort":
            result=False
            break
    
    if result==True:
        print "ALL SUBLOCKS ACQUIRED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Success")
    else :
        print "TRYLOCK ABORTED AT "+settings.SERVER_IP+":"+settings.SERVER_PORT
        
        return HttpResponse("Abort")

def items_release(request):
    pass