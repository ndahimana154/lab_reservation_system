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
    return render(request,'reservations/home.html')

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
