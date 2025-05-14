from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from .form import RegistartionForm,LoginForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistartionForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            print("Form is not valid")
    else:
        form = RegistartionForm()
    return render(request, "accounts/registration.html", {"form": form})

def login(request):
    form=LoginForm()
    home = reverse("home")

    if request.user.is_authenticated:
        return HttpResponseRedirect(home)
    else:

        if request.method == 'POST':
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.changed_data['password']

                print(username)
                print(password)
                user=authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect(home)
            else:
                print("invalid form data")
        else:
            form=LoginForm()
        context={"form":form}
        return render(request,"accounts/login.html",context)
