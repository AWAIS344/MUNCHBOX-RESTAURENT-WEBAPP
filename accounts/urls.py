from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from.form import LoginFrom

urlpatterns = [
    path("register/",views.register,name="register"),
    path("login/",LoginView.as_view(template_name="accounts/login.html",authentication_form=LoginFrom),name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),

]
