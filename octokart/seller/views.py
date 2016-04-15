from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from seller.models import CatalogueItem, SellerItem
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from seller.forms import UserForm
import ast
# Create your views here.

@login_required
def get_catalogue(request):
    # user = request.user
    # if user.is_active == 1:
    print "get_catalogue"
    cataloguedb = CatalogueItem.objects.all()
    
    catalogue={}
    
    for c in cataloguedb:
        catalogue[c.id]={'name':c.name, 'desc':c.desc, 'upvotes':c.upvotes}
    
    return JsonResponse(catalogue)
    # else:
    #     print "User not authenticated"
    #     return JsonResponse({"failure":"failure"})

@login_required
def sync_catalogue(request):
    # if user.is_active==1:
    seller_id = request.user
    itemDict = request.GET.dict()
    # seller_id = itemDict['0']
    # seller_id = User.objects.get(id=seller_id)
    try: 
        seller_exist = SellerItem.objects.filter(seller_id=seller_id)
        for key in itemDict:
            if int(key)!=0:
                item_id = CatalogueItem.objects.get(id=int(key))
                item_count = itemDict[key]
                try:
                    sellerItem = SellerItem.objects.get(seller_id=seller_id,item_id=item_id)
                    sellerItem.quantity = item_count
                    sellerItem.save()
                except SellerItem.DoesNotExist:
                    sellerItem = SellerItem.objects.create(seller_id=seller_id,item_id=item_id,quantity=item_count)
                    sellerItem.save()
        return JsonResponse({'success':'success'})
    #update the existing list
    except SellerItem.DoesNotExist:
        #create the seller id and add each item to list
        for key in itemDict:
            if int(key)!=0:
                item_id = CatalogueItem.objects.get(id=int(key))
                item_count = itemDict[key]
                sellerItem = SellerItem.objects.create(seller_id=seller_id,item_id=item_id,quantity=item_count)
                sellerItem.save()
        return JsonResponse({'success':'success'})
    # else:
    #     print "Not an active user"
    #     return JsonResponse({'failure':'failure'})
    # print request.body
        # myDict = dict(sellerdict.iterlists())
    # print myDict
    # print "###############################################"
    # print sellerdict 
    

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
        return redirect('/seller/login/')
    else:
        user_form = UserForm()
        return render(request, 'seller/register.html', {'user_form': user_form, 'registered': registered} )

def login(request):
    print "login called"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('/octokartseller/')
            else:
                return HttpResponse("Your Octokart account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        print request.user.is_authenticated()
        return render(request, 'seller/login.html', {})

@login_required    
def logout(request):
    auth_logout(request)
    return HttpResponse("Logged Out.")