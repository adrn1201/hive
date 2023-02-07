from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wholesaler

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ['email','username','password1','password2']
        
        

class WholesalerCreationForm(ModelForm):
    class Meta: 
        model = Wholesaler 
        exclude = ['schema_name', 'domain', 'is_active', 'user']
