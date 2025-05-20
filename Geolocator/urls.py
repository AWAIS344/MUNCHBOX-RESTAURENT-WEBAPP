from django.urls import path, include
from .views import GeoLocator

urlpatterns = [
    
    path('locator/', GeoLocator , name="locator" ),
]
