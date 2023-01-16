from django.forms import ModelForm
from .models import Inventory, Category


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['tempo_quantity']
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        