from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from .form import RegistartionForm,LoginForm
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistartionForm(request.POST)
        if form.is_valid():
            user=form.save()
            # login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            print("Form is not valid")
    else:
        form = RegistartionForm()
    return render(request, "accounts/registration.html", {"form": form})

def login_view(request):
    home = reverse("home")

    if request.user.is_authenticated:
        return HttpResponseRedirect(home)

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Use AuthenticationForm's built-in authentication
            if user is not None:
                login(request, user, backend='accounts.backends.EmailBackend')
                return HttpResponseRedirect(home)
            else:
                form.add_error(None, "Invalid email or password.")
        else:
            form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "accounts/login.html", context)