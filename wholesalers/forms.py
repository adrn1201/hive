from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.contrib.auth.models import User
from .models import Wholesaler
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ['email','username','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})    
    

        
class WholesalerCreationForm(ModelForm):

    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter business name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street / Building Name'}))
    # region = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Region'}))
    # city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zamboanga City'}))
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter contact persons name'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

    class Meta: 
        model = Wholesaler 
        exclude = ['schema_name', 'domain', 'is_active', 'is_wholesaler', 'user']
        readonly_fields = ('city', 'region')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
