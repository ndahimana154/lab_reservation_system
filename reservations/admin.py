from django.contrib import admin # type: ignore
from .models import LabEquipmentType, LabEquipment, Reservation, CustomUser
from django.contrib.auth.admin import UserAdmin # type: ignore

admin.site.register(LabEquipmentType)
admin.site.register(LabEquipment)
admin.site.register(Reservation)

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
