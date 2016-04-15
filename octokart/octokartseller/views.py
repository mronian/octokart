from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def mainpage(request):
	print "Hello world"
	return render(request, "store/homepage.html")
