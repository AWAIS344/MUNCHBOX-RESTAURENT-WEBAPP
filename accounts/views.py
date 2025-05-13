from django.shortcuts import render
from .form import RegistartionForm,LoginFrom

# Create your views here.
def register(request):
    form=RegistartionForm()
    context={"form":form}
    return render(request,"accounts/registration.html",context)

def login(request):
    form=LoginFrom()
    context={"form":form}
    return render(request,"accounts/login.html",context)
