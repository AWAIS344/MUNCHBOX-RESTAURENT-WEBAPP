from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django import forms
from django.contrib.auth.models import User

class RegistartionForm(UserCreationForm):

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g Awais"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g Ali"}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"xyz123@gmail.com"}))
    password1=forms.CharField( widget=forms.PasswordInput(attrs={"placeholder":"e.g ********" , "class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"e.g ********" , "class":"form-control"}))

    class Meta:
        model = User
        fields = ["username","first_name","last_name","Email"]
        widgets={
            "username":forms.TextInput(attrs={"placeholder":"e.g awais8900" , "class":"form-control"}),
        }

class LoginFrom(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g Awais Ali","autofocus":True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"e.g ********"}))
