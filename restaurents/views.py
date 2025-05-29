from django.shortcuts import render
from .forms import AddRestaurentForm,Package
from core.models import Package
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .forms import AddRestaurentForm
from core.models import Package, Restaurant, Cuisine
from .serializers import RestaurantSerializer

from django.contrib import messages


# Create your views here.
def RestaurentHome(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
    return render(request, 'restaurents/restaurant.html', {'restaurant': restaurant})

@login_required
def AddRestaurent(request):
    """
    View to handle the multi-step restaurant registration process.
    """
    packages = Package.objects.all()
    form_data = request.session.get('restaurant_form_data', {})
    form = AddRestaurentForm(request.POST or form_data)
    current_step = request.session.get('current_step', '1')

    if request.method == 'POST':
        step = request.POST.get('step', '1')

        if step == '1':  
            if form.is_valid():
             
                cleaned_data = form.cleaned_data.copy()
                cleaned_data['cuisines'] = [cuisine.id for cuisine in form.cleaned_data['cuisines']]
                request.session['restaurant_form_data'] = cleaned_data
                request.session['current_step'] = '2'
                return render(request, 'restaurents/add_restaurent.html', {
                    'form': AddRestaurentForm(),
                    'package': packages,
                    'current_step': '2',
                    'current_user': request.user
                })
            else:
                messages.error(request, 'Please correct the errors in the form.')
                current_step = '1'

        elif step == '2': 
            package_id = request.POST.get('package_id')
            if package_id:
                try:
                    package = Package.objects.get(id=package_id)
                    request.session['selected_package'] = package_id
                    request.session['current_step'] = '3'
                    return render(request, 'restaurents/add_restaurent.html', {
                        'form': AddRestaurentForm(),
                        'package': packages,
                        'current_step': '3',
                        'current_user': request.user
                    })
                except Package.DoesNotExist:
                    messages.error(request, 'Invalid package selected.')
            else:
                messages.error(request, 'Please select a package.')
            current_step = '2'

        elif step == '3':  # Payment
            form_data = request.session.get('restaurant_form_data')
            if form_data:
                form = AddRestaurentForm(form_data)
                if form.is_valid():
                    request.session['current_step'] = '4'
                    return render(request, 'restaurents/add_restaurent.html', {
                        'form': AddRestaurentForm(),
                        'package': packages,
                        'current_step': '4',
                        'current_user': request.user
                    })
                else:
                    messages.error(request, 'Invalid form data. Please start over.')
                    current_step = '1'
            else:
                messages.error(request, 'No form data found. Please start over.')
                current_step = '1'

        elif step == '4':  # Save & Preview
            form_data = request.session.get('restaurant_form_data')
            package_id = request.session.get('selected_package')
            if form_data and package_id:
                # Reconstruct form data for saving
                form_data_copy = form_data.copy()
                cuisines_ids = form_data_copy.pop('cuisines')
                form = AddRestaurentForm(form_data_copy)
                if form.is_valid():
                    restaurant = form.save(commit=False)
                    restaurant.owner = request.user
                    restaurant.package = Package.objects.get(id=package_id)
                    restaurant.save()
                    # Save cuisines (ManyToMany field)
                    restaurant.cuisines.set(Cuisine.objects.filter(id__in=cuisines_ids))
                    
                    # Clear session data
                    request.session.pop('restaurant_form_data', None)
                    request.session.pop('selected_package', None)
                    request.session.pop('current_step', None)
                    
                    messages.success(request, 'Restaurant registered successfully!')
                    return redirect('restaurant_preview', restaurant_id=restaurant.id)
                else:
                    messages.error(request, 'Invalid form data. Please start over.')
                    current_step = '1'
            else:
                messages.error(request, 'Incomplete data. Please start over.')
                current_step = '1'

        else:
            messages.error(request, 'Invalid step.')
            current_step = '1'

    return render(request, 'restaurents/add_restaurent.html', {
        'form': AddRestaurentForm(),
        'package': packages,
        'current_step': current_step,
        'current_user': request.user
    })

# DRF API View
class RestaurantListCreateAPIView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

def RestaurentList(request):
    context={}
    return render(request,"restaurents/listview.html",context)



    