from django.shortcuts import render, redirect

# Create your views here.
def display_store(request):
    context_dict = {}
    context_dict["seller_id"]="1"
    return render(request, 'store/homepage.html', context_dict)

