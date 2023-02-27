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
    
    # def username_clean(self):  
    #     username = self.cleaned_data['username'].lower()  
    #     new = User.objects.filter(username = username)  
    #     if new.count():  
    #          self.add_error('username', "some message")  
    #     return username  
  
    # def email_clean(self):  
    #     email = self.cleaned_data['email'].lower()  
    #     new = User.objects.filter(email=email)  
    #     if new.count():  
    #         raise ValidationError(" Email Already Exist")  
    #     return email  
  
    # def clean_password2(self):  
    #     password1 = self.cleaned_data['password1']  
    #     password2 = self.cleaned_data['password2']  
  
    #     if password1 and password2 and password1 != password2:  
    #         raise ValidationError("Password don't match")  
    #     return password2  
  
    # def save(self, commit = True):  
    #     user = User.objects.create_user(  
    #         self.cleaned_data['username'],  
    #         self.cleaned_data['email'],  
    #         self.cleaned_data['password1']  
    #     )  
    #     return user  
        

class WholesalerCreationForm(ModelForm):

    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter business name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Area and Street'}))
    region = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your Region'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your City'}))
    contact_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter contact persons name'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

    class Meta: 
        model = Wholesaler 
        exclude = ['schema_name', 'domain', 'is_active', 'is_wholesaler', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})