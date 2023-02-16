from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Retailer
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        model = User 
        fields = ['email','username','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 
        

class RetailerCreationForm(ModelForm):
    class Meta: 
        model = Retailer 
        exclude = ['is_active', 'wholesaler', 'user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})