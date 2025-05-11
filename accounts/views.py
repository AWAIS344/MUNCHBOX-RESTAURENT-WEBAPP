from django.shortcuts import render
from .form import RegistartionForm

# Create your views here.
def register(request):
    form=RegistartionForm()
    context={"form":form}
    return render(request,"accounts/login.html",context)