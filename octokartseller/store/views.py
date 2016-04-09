from django.shortcuts import render, redirect

# Create your views here.
def display_store(request):
    context_dict={}
    return render(request, 'store/homepage.html', context_dict)

def register(request):
    