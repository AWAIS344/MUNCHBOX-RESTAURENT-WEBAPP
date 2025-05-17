from django.urls import path, include
from .views import OrderCheckout
urlpatterns = [
    
    path('checkout/', OrderCheckout , name="checkout" ),
]
