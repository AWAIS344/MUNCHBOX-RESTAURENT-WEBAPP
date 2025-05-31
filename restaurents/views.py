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
import json
from django.contrib import messages


# Create your views here.
def RestaurentHome(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
    return render(request, 'restaurents/restaurant.html', {'restaurant': restaurant})

@login_required
def AddRestaurent(request):
    # Get session data
    form_data = request.session.get('restaurant_data', {})
    # Initialize form with session data
    form = AddRestaurentForm(form_data or None)
    packages = Package.objects.all()
    cuisines = Cuisine.objects.all()

    # Get or set current step
    current_step = request.session.get('current_step', '1')

    # Debug: Log session data
    print("Session restaurant_data:", form_data)

    if request.method == 'POST':
        step = request.POST.get('step')

        if step == '2' and current_step == '1':
            form = AddRestaurentForm(request.POST)
            if form.is_valid():
                # Save form data to session
                restaurant_data = form.cleaned_data.copy()
                restaurant_data.pop('terms_accepted', None)  # Remove non-model field
                # Store cuisines as list of IDs
                restaurant_data['cuisines'] = [cuisine.id for cuisine in restaurant_data['cuisines']]
                request.session['restaurant_data'] = restaurant_data
                request.session['current_step'] = '2'
                request.session.modified = True
                messages.success(request, "Step 1 completed successfully.")
                # Initialize new form for Step 2, but keep session data
                return render(request, 'restaurents/add_restaurant.html', {
                    'form': AddRestaurentForm(form_data),
                    'packages': packages,
                    'cuisines': cuisines,
                    'current_step': '2',
                    'current_user': request.user,
                    'session_data': json.dumps(form_data)  # Pass for JS debugging
                })
            else:
                messages.error(request, "Please correct the errors below.")
                print("Form errors:", form.errors)
                current_step = '1'

        elif step == '3' and current_step == '2':
            package_id = request.POST.get('package_id')
            if package_id:
                request.session['package_id'] = package_id
                request.session['current_step'] = '3'
                request.session.modified = True
                messages.success(request, "Package selected successfully.")
                return render(request, 'restaurents/add_restaurant.html', {
                    'form': AddRestaurentForm(form_data),  # Use session data
                    'packages': packages,
                    'cuisines': cuisines,
                    'current_step': '3',
                    'current_user': request.user,
                    'session_data': json.dumps(form_data)
                })
            else:
                messages.error(request, "Please select a package.")
                current_step = '2'

        elif step == '4' and current_step == '3':
            request.session['current_step'] = '4'
            request.session.modified = True
            messages.success(request, "Payment step reached.")
            return render(request, 'restaurents/add_restaurant.html', {
                'form': AddRestaurentForm(form_data),  # Use session data
                'packages': packages,
                'cuisines': cuisines,
                'current_step': '4',
                'current_user': request.user,
                'session_data': json.dumps(form_data)
            })

        elif step == '4' and current_step == '4':
            restaurant_data = request.session.get('restaurant_data', {})
            package_id = request.session.get('package_id')
            if restaurant_data and package_id:
                try:
                    restaurant = Restaurant(
                        owner=request.user,
                        name=restaurant_data.get('name'),
                        phone=restaurant_data.get('phone', ''),
                        manager_name=restaurant_data.get('manager_name', ''),
                        manager_phone=restaurant_data.get('manager_phone', ''),
                        contact_email=restaurant_data.get('contact_email', ''),
                        country=restaurant_data.get('country', ''),
                        state=restaurant_data.get('state', ''),
                        city=restaurant_data.get('city', ''),
                        latitude=restaurant_data.get('latitude'),
                        longitude=restaurant_data.get('longitude'),
                        address=restaurant_data.get('address', ''),
                        delivery_pickup=restaurant_data.get('delivery_pickup', ''),
                        package_id=package_id
                    )
                    restaurant.save()
                    # Restore cuisines
                    cuisine_ids = restaurant_data.get('cuisines', [])
                    restaurant.cuisines.set(cuisine_ids)
                    messages.success(request, "Restaurant created successfully!")
                    # Clear session
                    request.session.pop('restaurant_data', None)
                    request.session.pop('package_id', None)
                    request.session['current_step'] = '1'
                    request.session.modified = True
                    return redirect('restaurant_preview')  # Replace with your URL
                except Exception as e:
                    messages.error(request, f"Error creating restaurant: {str(e)}")
                    current_step = '4'
            else:
                messages.error(request, "Incomplete data. Please start over.")
                request.session['current_step'] = '1'
                current_step = '1'

        # Handle Previous steps
        elif step in ['1', '2', '3']:
            request.session['current_step'] = step
            request.session.modified = True
            current_step = step

    # GET request or invalid POST
    return render(request, 'restaurents/add_restaurant.html', {
        'form': form,
        'packages': packages,
        'cuisines': cuisines,
        'current_step': current_step,
        'current_user': request.user,
        'session_data': json.dumps(form_data)
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



    