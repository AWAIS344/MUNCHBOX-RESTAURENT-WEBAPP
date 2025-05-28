# core/forms.py
from django import forms
from core.models import Restaurant, Package

class AddRestaurentForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ["owner"]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Restaurant Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Phone Number'}),
            'manager_name': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Manager Name'}),
            'manager_phone': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Manager Phone'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Email'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'City'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Longitude'}),
            'delivery_pickup': forms.Select(attrs={'class': 'form-control form-control-submit'}),
            'cuisines': forms.SelectMultiple(attrs={'class': 'form-control form-control-submit'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-submit'}),
        }

class Package_form(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'