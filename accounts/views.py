from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from .form import RegistrationForm,LoginForm
from django.contrib.auth.models import User
from core.models import Profile

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            Profile.objects.create(
                user=user,
                city=form.cleaned_data.get('city')
            )
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            print("Form is not valid")
    else:
        form = RegistrationForm()
    return render(request, "accounts/registration.html", {"form": form})

def login_view(request):
    home = reverse("home")

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return HttpResponseRedirect(home)


    if request.method == 'POST':
        print("Form data:", request.POST)  # Debug form input
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                    login(request,user)
                    
                    return HttpResponseRedirect(home)
            else:
                print("Authentication failed: user is None")
        else:
            print("Form errors:", form.errors)
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))