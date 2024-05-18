from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.utils import timezone # type: ignore
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore

from .models import LabEquipment, LabEquipmentType, Reservation
from .forms import *


def index(request):
    equipment_types = LabEquipmentType.objects.all()
    return render(request, 'reservations/index.html', {'equipment_types': equipment_types})

# Registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                if user.role == 'lab_tech':
                    return redirect('home')  # Redirect to the home page for lab technicians
                else:
                    return redirect('client')  # Redirect to the client page for standard users
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def home_view (request):
    total_equipments = LabEquipment.objects.count()
    equipment_list = LabEquipment.objects.all() if request.user.is_authenticated and request.user.role == 'standard' else []
    context = {
        'total_equipments': total_equipments,
        'equipment_list': equipment_list,
    }
    return render(request,'reservations/home.html',context)

def equipments_view(request):
    equipments = LabEquipment.objects.all()
    return render(request, 'reservations/equipments.html', {'equipments': equipments})


def update_equipment_view(request, equipment_id):
    equipment = get_object_or_404(LabEquipment, pk=equipment_id)
    if request.method == 'POST':
        form = LabEquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipments')  # Redirect to the list of equipment
    else:
        form = LabEquipmentForm(instance=equipment)
    return render(request, 'reservations/update_equipment.html', {'form': form})

# Delete equipment Function
def delete_equipment_view(request, pk):
    # Retrieve the equipment object or return 404 if not found
    equipment = get_object_or_404(LabEquipment, pk=pk)

    # Delete the equipment object
    equipment.delete()
    # Redirect to the equipment list page
    return redirect('equipments')  # Replace 'equipment_list' with the name of your equipment list URL pattern

# Create equipment 
def create_equipment_view(request):
    
     # Retrieve all equipment types from the database
    equipment_types = LabEquipmentType.objects.all()

    # Pass the equipment types to the template context
    context = {'equipment_types': equipment_types}


    return render(request,'reservations/new_equipment.html',context)
   
def create_equipment(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    quantity = 1
    type_id = request.POST.get('type')
    equipment_type = LabEquipmentType.objects.get(pk=type_id)
    # Create a new LabEquipment object
    equipment = LabEquipment.objects.create(
        name=name,
        description=description,
        quantity=quantity,
        type=equipment_type
    )

    # Return a JSON response indicating success
    return redirect('equipments')

def logout_for_tech(request):
    return redirect('login')






# Equipments Typws


def equipments_types_view(request):
    equipments_types = LabEquipmentType.objects.all()
    return render(request,'reservations/equipments_types.html', {'equipments_types':equipments_types})
def equipments_types_form_view(request):
    return render(request,'reservations/new_equipment_type.html')

def new_equipment_type(request):
    if request.method == 'POST':
        form = LabEquipmentTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipments_types')  # Redirect to the equipment types page after saving
    else:
        form = LabEquipmentTypeForm()
    return render(request, 'reservations/new_equipment_type.html', {'form': form})


def equipment_detail(request, pk):
    equipment = get_object_or_404(LabEquipment, pk=pk)
    return render(request, 'reservations/equipment_detail.html', {'equipment': equipment})

def create_equipment_type(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        description = data.get('description')

        # Validate form data
        if name and description:
            # Create and save LabEquipmentType instance
            equipment_type = LabEquipmentType.objects.create(name=name, description=description)
            return redirect('equipments_types')
        else:
            return JsonResponse({'success': False, 'message': 'Name and description are required'})

    # Handle invalid request method
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_equipment_type_view(request, equipment_type_id):
    equipment_type = get_object_or_404(LabEquipmentType, pk=equipment_type_id)
    if request.method == 'POST':
        form = LabEquipmentTypeForm(request.POST, instance=equipment_type)
        if form.is_valid():
            form.save()
            return redirect('equipments_types')  # Redirect to the list of equipment types
    else:
        form = LabEquipmentTypeForm(instance=equipment_type)
    return render(request, 'reservations/update_equipment_type.html', {'form': form})


@login_required
def reserve_equipment(request, pk):
    equipment = get_object_or_404(LabEquipment, pk=pk)
    if request.method == 'POST':
        reserved_quantity = int(request.POST['reserved_quantity'])
        if reserved_quantity <= equipment.available_quantity:
            reservation = Reservation.objects.create(
                user=request.user,
                equipment=equipment,
                reserved_quantity=reserved_quantity,
                reserved_date=timezone.now()
            )
            equipment.available_quantity -= reserved_quantity
            equipment.save()
            return redirect('index')
    return render(request, 'reservations/reserve_equipment.html', {'equipment': equipment})




























def home(request):
    return render(request, 'indexes.html')




















def signup(request): 
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})



def request_equipment_view(request, equipment_id):
    # Get the equipment object
    equipment = get_object_or_404(LabEquipment, id=equipment_id)

    # Update equipment quantity to 0
    equipment.quantity = 0
    equipment.save()

    # Create a reservation for the user
    reservation = Reservation.objects.create(
        user=request.user,
        equipment=equipment,
        reserved_quantity=1,
        reserved_date=timezone.now()  # Adjust the time as needed
    )

    # Save the reservation
    reservation.save()

    # Provide a success message
    messages.success(request, 'Equipment requested successfully.')

    # Redirect back to the home page or any other page
    return redirect('equipments')


def view_reservations(request):
     # Fetch all reservations
    reservations = Reservation.objects.all()

    # You can further process the reservations or pass them directly to the template
    context = {
        'reservations': reservations
    }

    # Render the template with the reservations data
    return render(request, 'reservations/reservations.html', context)


def confirm_reservation(request,reservation_id):
    # Retrieve the reservation object
    reservation = Reservation.objects.get(id=reservation_id).order_by('-reserved_date')

    # Confirm the reservation
    reservation.confirmed = True
    reservation.save()

    # Update the stock of the equipment to zero
    equipment = reservation.equipment
    equipment.quantity = 0
    equipment.save()

    # Redirect to a success page or any other appropriate page
    return redirect('reservations_view')


def mark_return(request, reservation_id):
    # Retrieve the reservation object
    reservation = Reservation.objects.get(id=reservation_id)

    # Mark the reservation as returned
    reservation.is_returned = True
    reservation.save()

    # Increment the quantity of the equipment by 1
    equipment = reservation.equipment
    equipment.quantity = 1
    equipment.save()

    # Redirect to a success page or any other appropriate page
    return redirect('reservations_view')

def view_user_reservations(request):
    # Fetch reservations for the current user
    user_reservations = Reservation.objects.filter(user=request.user).order_by('-reserved_date')

    # Pass the user reservations to the template
    context = {
        'user_reservations': user_reservations
    }

    # Render the template with the user reservations data
    return render(request, 'reservations/user_reservations.html', context)