from django.urls import path, include
from .views import RestaurentDeals

urlpatterns = [
    
    path('deals/', RestaurentDeals , name="deals" ),
]


