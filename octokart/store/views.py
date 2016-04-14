from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def get_index(request):
	context = {}
	return render(request, 'store_index.html',context)
