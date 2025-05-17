from django.shortcuts import render

# Create your views here.
def OrderCheckout(request):
    context={}
    return render(request,"order/checkout.html",context)