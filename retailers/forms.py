from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Retailer
from django.forms import ModelForm
from django.forms import TextInput
from django import forms
from django.core.exceptions import ValidationError



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta: 
        model = User 
        fields = ['email','username','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Email is already in use.')
        return email
        

class RetailerCreationForm(ModelForm):

    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter business name'}), required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Street / Building Name'}), required=False)
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter contact persons name'}), required=False)
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}), required=False)

    class Meta: 
        model = Retailer 
        exclude = ['is_active', 'wholesaler', 'user']
        readonly_fields = ('city', 'region')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

