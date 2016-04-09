from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from seller.models import CatalogueItem
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from seller.forms import UserForm
# Create your views here.

def get_catalogue(request):
    cataloguedb = CatalogueItem.objects.all()
    
    catalogue={}
    
    for c in cataloguedb:
        catalogue[c.id]={'name':c.name, 'desc':c.desc, 'upvotes':c.upvotes}
    
    return JsonResponse(catalogue)

def sync_catalogue(request):
    
    sellercatalogue=json.dumps(request.GET)
    
    print request.user.is_authenticated()
    
    return JsonResponse({'success':'success'})

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('/')
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