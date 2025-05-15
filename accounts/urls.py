from django.urls import path
from .api import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
    # Existing form-based URLs
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_logout, name='logout'),
]