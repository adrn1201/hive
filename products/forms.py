from django.forms import ModelForm
from .models import Inventory, Category
from django import forms;


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['tempo_quantity', 'with_size', 'size']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
