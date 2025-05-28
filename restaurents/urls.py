from django.urls import path
from .views import RestaurentHome,AddRestaurent,RestaurentList,AddRestaurent, RestaurantListCreateAPIView, restaurant_preview

urlpatterns = [

    path('restaurent/', RestaurentHome , name="rest_home" ),
    path('add-restaurant/', AddRestaurent, name='add_rest'),
    path('api/restaurants/', RestaurantListCreateAPIView.as_view(), name='restaurant-api'),
    path('restaurant/preview/<int:restaurant_id>/', restaurant_preview, name='restaurant_preview'),
    path('restaurentlist/', RestaurentList , name="list_view" ),
    
]