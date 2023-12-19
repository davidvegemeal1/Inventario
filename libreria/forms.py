from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import monitoreo_del_conteo

class CustomUserCreationForm(UserCreationForm):
   
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class inventarioform(forms.ModelForm):
    class Meta:
        model = monitoreo_del_conteo
        fields='__all__'
