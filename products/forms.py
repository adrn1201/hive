from django.forms import ModelForm
from .models import Inventory, Category


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['tempo_quantity', 'wholesaler', 'sold']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['wholesaler', 'sold']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        