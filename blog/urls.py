from django.urls import path
from .views import BlogHome
# from .api import RegisterAPIView, LoginAPIView, LogoutAPIView


urlpatterns = [
    path('blog/', BlogHome, name='blog'),
]