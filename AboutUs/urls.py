from django.urls import path, include
from .views import AboutUs

urlpatterns = [
    
    path('aboutus/',AboutUs,name="aboutus"),
]


