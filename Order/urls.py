from django.urls import path, include
from .views import OrderCheckout,OrderDetails
urlpatterns = [
    
    path('checkout/', OrderCheckout , name="checkout" ),
    path('orderdetail/', OrderDetails , name="order_detail" ),
]
