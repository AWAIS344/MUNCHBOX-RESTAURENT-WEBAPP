from django.shortcuts import render
from .forms import AddRestaurentForm

# Create your views here.
def RestaurentHome(request):
    context={}

    return render(request,"restaurents/restaurent.html",context)

def AddRestaurent(request):
    form = AddRestaurentForm()

    context={"form":form}
    return render(request,"restaurents/add_restaurent.html",context)

def RestaurentList(request):
    context={}
    return render(request,"restaurents/listview.html",context)



    