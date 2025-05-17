from django.shortcuts import render

# Create your views here.
def RestaurentDeals(request):
    context={}
    return render(request,"ExDeals/ex_deals.html",context)