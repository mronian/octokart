from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from seller.models import SellerItem
from seller.models import CatalogueItem
from transactions.views import perform_transaction

# Create your views here.
def get_index(request):
        context = {}
        print "get index"
        return render(request, 'store/store_index.html',context)
    
def get_item(request, item_id):
	items = SellerItem.objects.filter(item_id=item_id)
	catalog = CatalogueItem.objects.get(id=item_id)
	item_list = list()
	for item in items:
		item_list.append((str(item.seller_id.username), int(item.quantity)))
	context = {'item_id': int(item_id), 'item_name': str(catalog.name),  'item_desc' : str(catalog.desc), 'upvotes' : catalog.upvotes, 'items': item_list}
	return render(request, 'store/specific_item.html',context)

def get_catalogue(request):
    # user = request.user
    # if user.is_active == 1:
    print "get_catalogue"
    cataloguedb = CatalogueItem.objects.all()
    catalogue={}
    items = {}

    for c in cataloguedb:
        selleritemdb = SellerItem.objects.filter(item_id=c)
        sum1 = 0
        for s in selleritemdb:
             sum1 += s.quantity
        catalogue[c.id]={'name':c.name, 'desc':c.desc, 'upvotes':c.upvotes, 'quantity':sum1}
    return JsonResponse(catalogue)
    # else:
    #     print "User not authenticated"
    #     return JsonResponse({"failure":"failure"})

def buy_item(request):
    
    seller_name=request.GET['seller_name']
    item_name=request.GET['item_name']
    q=int(request.GET['quantity'])
    
    seller=User.objects.get(username=seller_name)
    item=CatalogueItem.objects.get(name=item_name)
    
    sellerItem = SellerItem(seller_id=seller,item_id=item,quantity=q)
    
    perform_transaction(None, None, sellerItem)
    
    return redirect('/store/')