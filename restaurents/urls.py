from django.urls import path
from .views import RestaurentHome,AddRestaurent,RestaurentDeals

urlpatterns = [

    path('restaurent/', RestaurentHome , name="rest_home" ),
    path('add_restaurent/', AddRestaurent , name="add_rest" ),
    path('deals/', RestaurentDeals , name="deals" ),
]