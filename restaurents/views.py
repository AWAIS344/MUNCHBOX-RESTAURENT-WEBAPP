from django.shortcuts import render

# Create your views here.
def RestaurentHome(request):
    context={}

    return render(request,"restaurents/restaurent.html",context)