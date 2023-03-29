from django.forms import ModelForm
from django import forms
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.choices = [choice for choice in self.fields['status'].widget.choices if choice[0] != 'pending']
        self.fields['status'].widget.choices = [choice for choice in self.fields['status'].widget.choices if choice[0] != 'completed']
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    