from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}), required=False)
    
    class Meta: 
        model = User 
        fields = ['first_name','last_name', 'email', 'username','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control rounded-9'})
