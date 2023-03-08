from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Retailer
from django.forms import ModelForm
from django.forms import TextInput
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ['email','username','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 
        

class RetailerCreationForm(ModelForm):

    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter business name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street / Building Name'}))
    # region = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Region'}))
    # city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your City'}))
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter contact persons name'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

    class Meta: 
        model = Retailer 
        exclude = ['is_active', 'wholesaler', 'user']
        readonly_fields = ('city', 'region')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

