from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth.models import User # type: ignore

from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    
class LabEquipmentTypeForm(forms.ModelForm):
    class Meta:
        model = LabEquipmentType
        fields = ['name', 'description']
        
class LabEquipmentForm(forms.ModelForm):
    class Meta:
        model = LabEquipment
        fields = ['name', 'description', 'quantity', 'type']