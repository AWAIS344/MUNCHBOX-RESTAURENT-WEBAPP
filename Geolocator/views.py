from django.shortcuts import render

# Create your views here.
def GeoLocator(request):
    context={}
    return render(request,"geolocator/geolocator.html",context)
