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
    # Initialize form and packages
    form_data = request.session.get('restaurant_data', {})
    form = RestaurantForm(request.POST or form_data)
    packages = Package.objects.all()
    
    # Get or set current step
    current_step = request.session.get('current_step', '1')
    
    if request.method == 'POST':
        step = request.POST.get('step')
        
        if step == '2' and current_step == '1':
            if form.is_valid():
                # Save form data to session
                request.session['restaurant_data'] = form.cleaned_data
                request.session['current_step'] = '2'
                request.session.modified = True
                messages.success(request, "Step 1 completed successfully.")
                return render(request, 'restaurents/add_restaurant.html', {
                    'form': RestaurantForm(),  # Reset form for next steps
                    'packages': packages,
                    'current_step': '2',
                    'current_user': request.user
                })
            else:
                messages.error(request, "Please correct the errors below.")
                print(form.errors)  # Debug: Log form errors to console
                current_step = '1'
        
        elif step == '3' and current_step == '2':
            package_id = request.POST.get('package_id')
            if package_id:
                request.session['package_id'] = package_id
                request.session['current_step'] = '3'
                request.session.modified = True
                messages.success(request, "Package selected successfully.")
                return render(request, 'restaurents/add_restaurant.html', {
                    'form': RestaurantForm(),
                    'packages': packages,
                    'current_step': '3',
                    'current_user': request.user
                })
            else:
                messages.error(request, "Please select a package.")
                current_step = '2'
        
        elif step == '4' and current_step == '3':
            # Placeholder for payment processing
            request.session['current_step'] = '4'
            request.session.modified = True
            messages.success(request, "Payment step reached.")
            return render(request, 'restaurents/add_restaurant.html', {
                'form': RestaurantForm(),
                'packages': packages,
                'current_step': '4',
                'current_user': request.user
            })
        
        elif step == '4' and current_step == '4':
            # Save restaurant to database
            restaurant_data = request.session.get('restaurant_data', {})
            package_id = request.session.get('package_id')
            if restaurant_data and package_id:
                try:
                    restaurant = Restaurant.objects.create(
                        name=restaurant_data.get('name'),
                        phone=restaurant_data.get('phone'),
                        manager_name=restaurant_data.get('manager_name'),
                        manager_phone=restaurant_data.get('manager_phone'),
                        contact_email=restaurant_data.get('contact_email'),
                        country=restaurant_data.get('country'),
                        state=restaurant_data.get('state'),
                        city=restaurant_data.get('city'),
                        latitude=restaurant_data.get('latitude'),
                        longitude=restaurant_data.get('longitude'),
                        address=restaurant_data.get('address'),
                        delivery_pickup=restaurant_data.get('delivery_pickup'),
                        cuisines=restaurant_data.get('cuisines'),
                        user=request.user,
                        package_id=package_id
                    )
                    messages.success(request, "Restaurant created successfully!")
                    # Clear session data
                    request.session.pop('restaurant_data', None)
                    request.session.pop('package_id', None)
                    request.session['current_step'] = '1'
                    return redirect('restaurant_preview')  # Replace with your preview URL
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



    