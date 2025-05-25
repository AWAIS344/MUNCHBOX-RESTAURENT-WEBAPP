from django.shortcuts import render
from .forms import AddRestaurentForm,Package
from core.models import Package

from django.contrib import messages


# Create your views here.
def RestaurentHome(request):
    context={}

    return render(request,'restaurents/add_restaurent.html',context)

def AddRestaurent(request):
    """
    View to handle the multi-step restaurant registration process.
    """
    # Get all packages for the package selection step
    packages = Package.objects.all()
    
    # Initialize form with session data if available
    form_data = request.session.get('restaurant_form_data', {})
    form = AddRestaurentForm(request.POST or form_data)
    current_step = request.session.get('current_step', '1')

    # Handle form submission
    if request.method == 'POST':
        step = request.POST.get('step', '1')

        if step == '1':
            if form.is_valid():
                # Save form data to session
                request.session['restaurant_form_data'] = form.cleaned_data
                request.session['current_step'] = '2'
                return render(request, 'restaurents/add_restaurent.html', {
                    'form': form,
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
                    Package.objects.get(id=package_id)  # Validate package exists
                    request.session['selected_package'] = package_id
                    request.session['current_step'] = '3'
                    return render(request, 'restaurents/add_restaurent.html', {
                        'form': form,
                        'package': packages,
                        'current_step': '3',
                        'current_user': request.user
                    })
                except Package.DoesNotExist:
                    messages.error(request, 'Invalid package selected.')
            else:
                messages.error(request, 'Please select a package.')
            current_step = '2'

        elif step == '3':
            # Handle payment (placeholder)
            form_data = request.session.get('restaurant_form_data')
            if form_data:
                form = AddRestaurentForm(form_data)
                if form.is_valid():
                    restaurant = form.save(commit=False)
                    restaurant.user = request.user
                    package_id = request.session.get('selected_package')
                    if package_id:
                        restaurant.package = Package.objects.get(id=package_id)
                    restaurant.save()
                    
                    # Clear session data
                    request.session.pop('restaurant_form_data', None)
                    request.session.pop('selected_package', None)
                    request.session.pop('current_step', None)
                    
                    messages.success(request, 'Restaurant registered successfully!')
                    return render(request, 'restaurents/add_restaurent.html', {
                        'form': form,
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

        else:
            messages.error(request, 'Invalid step.')
            current_step = '1'

    # Handle GET request or invalid POST
    return render(request, 'restaurents/add_restaurent.html', {
        'form': form,
        'package': packages,
        'current_step': current_step,
        'current_user': request.user
    })

def RestaurentList(request):
    context={}
    return render(request,"restaurents/listview.html",context)



    