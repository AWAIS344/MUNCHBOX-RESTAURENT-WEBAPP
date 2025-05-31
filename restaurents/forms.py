from django import forms
from core.models import Restaurant, Package, Cuisine

class AddRestaurentForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label="Accept terms",
        widget=forms.CheckboxInput(attrs={'class': 'custom-checkbox'})
    )

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
            'address': forms.TextInput(attrs={'class': 'form-control form-control-submit', 'placeholder': 'Type Your Address'}),
            'delivery_pickup': forms.Select(
                attrs={'class': 'form-control form-control-submit'},
                choices=[('', 'Select Option'), ('delivery', 'Delivery'), ('pickup', 'Pickup'), ('both', 'Delivery & Pickup')]
            ),
            'cuisines': forms.SelectMultiple(attrs={'class': 'form-control form-control-submit'}),
            'package': forms.Select(attrs={'class': 'form-control form-control-submit'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cuisines'].queryset = Cuisine.objects.all()
        self.fields['package'].queryset = Package.objects.all()
        self.fields['package'].required = False  # Package is set in Step 2