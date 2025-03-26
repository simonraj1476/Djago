from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
class ContactFrom(forms.Form):
    name= forms.CharField(label="name",max_length=100,required=True)
    email = forms.EmailField(label="Email",required=True) 
    massage = forms.CharField(label='Massage',required=True)
    
class order(forms.Form):
    recipe_name = forms.CharField(label="recipe-name",max_length=100,required=True)
    quantity =forms.IntegerField(label="quantity", required=True)
    phone_number =forms.IntegerField(label="phone-number",required=True)
    location = forms.CharField(label="location", max_length=300, required=True)

