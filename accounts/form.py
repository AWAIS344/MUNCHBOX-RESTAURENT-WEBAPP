from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

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
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Custom password strength check
        if password1:
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r"\d", password1):
                raise ValidationError("Password must contain at least one number.")
            if not re.search(r"[A-Z]", password1):
                raise ValidationError("Password must contain at least one uppercase letter.")
            if not re.search(r"[a-z]", password1):
                raise ValidationError("Password must contain at least one lowercase letter.")

        return cleaned_data
    

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "e.g xyz@gmail.com", "autofocus": True}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "e.g ********"}),
        label="Password"
    )

    def confirm_login_allowed(self, user):
        # Optionally block inactive users
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code="inactive")