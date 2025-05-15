from django.urls import path
from .views import RestaurentHome

urlpatterns = [

    path('restaurent/', RestaurentHome , name="rest_home" ),
]