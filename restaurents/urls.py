from django.urls import path
from .views import RestaurentHome,AddRestaurent,RestaurentDeals,RestaurentList

urlpatterns = [

    path('restaurent/', RestaurentHome , name="rest_home" ),
    path('add_restaurent/', AddRestaurent , name="add_rest" ),
    path('restaurentlist/', RestaurentList , name="list_view" ),
    
]