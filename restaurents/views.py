from django.shortcuts import render
from .forms import AddRestaurentForm,Package
from core.models import Package

# Create your views here.
def RestaurentHome(request):
    context={}

    return render(request,"restaurents/restaurent.html",context)

def AddRestaurent(request):
    form = AddRestaurentForm()
    package=Package.objects.all()

    context={"form":form,"package":package}
    return render(request,"restaurents/add_restaurent.html",context)

def RestaurentList(request):
    context={}
    return render(request,"restaurents/listview.html",context)



    