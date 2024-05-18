from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/',views.home_view, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('equipments/', views.equipments_view, name='equipments'),
    # Update Equipment
    path('equipments/update/<int:equipment_id>/', views.update_equipment_view, name='update_equipment'),
    # Delete equipment
    path('equipment/delete/<int:pk>/', views.delete_equipment_view, name='delete_equipment'),
    # Create equipment vie
    path('equipment/create/', views.create_equipment_view, name='create_equipment'),
    # Create equipment
    path('equipment/new/save', views.create_equipment, name='new_equipment_save'),  
    path('equipments_types/', views.equipments_types_view, name='equipments_types'),
    path('equipments_types/new', views.equipments_types_form_view, name='new_equipment_type'),
     path('create_equipment_type/', views.create_equipment_type, name='create_equipment_type'),
    # Update the equipment type
     path('update/<int:equipment_type_id>/', views.update_equipment_type_view, name='update_equipment_type'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('reserve/<int:pk>/', views.reserve_equipment, name='reserve_equipment'),
    path('logout/', views.logout_for_tech, name='logouts'),
]
