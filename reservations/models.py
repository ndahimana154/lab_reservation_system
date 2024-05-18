from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore

class LabEquipmentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class LabEquipment(models.Model):
    type = models.ForeignKey(LabEquipmentType, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('lab_tech', 'Lab Technician'),
        ('standard', 'Standard User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='standard')

class Reservation(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    equipment = models.ForeignKey(LabEquipment, on_delete=models.CASCADE)
    reserved_quantity = models.PositiveIntegerField()
    reserved_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.equipment.name}"
