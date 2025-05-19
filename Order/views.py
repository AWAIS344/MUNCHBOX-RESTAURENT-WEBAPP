from django.shortcuts import render

# Create your views here.
def OrderCheckout(request):
    context={}
    return render(request,"order/checkout.html",context)

def OrderDetails(request):
    context={}
    return render(request,"order/order_detail.html",context)