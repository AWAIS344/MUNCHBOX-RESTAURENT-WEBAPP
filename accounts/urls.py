from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from .views import login_view
from.form import LoginForm

urlpatterns = [
    path("register/",views.register,name="register"),
   path('login/', login_view, name='login'),

]