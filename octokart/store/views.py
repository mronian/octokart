from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from seller.models import SellerItem
from seller.models import CatalogueItem
# Create your views here.
def get_index(request):
	context = {}
	return render(request, 'store_index.html',context)
def get_item(request, item_id):
	items = SellerItem.objects.filter(item_id=item_id)
	catalog = CatalogueItem.objects.get(id=item_id)
	item_list = list()
	for item in items:
		item_list.append((str(item.seller_id.username), int(item.quantity)))
	context = {'item_id': int(item_id), 'item_name': str(catalog.name),  'item_desc' : str(catalog.desc), 'upvotes' : catalog.upvotes, 'items': item_list}
	print context
	print item_id
	return render(request, 'specific_item.html',context)
