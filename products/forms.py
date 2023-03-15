from django.forms import ModelForm, inlineformset_factory
from .models import Product, Category, Variation
from wholesalers.models import Wholesaler


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            'category', 
            'product_image', 
            'product_name', 
            'description', 
            'price', 
            'min_orders', 
            'with_variation',
            'actual_stocks',
        )
        labels = {
            'actual_stocks': 'No. of Stocks',
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})
    
class VariationForm(ModelForm):
    class Meta:
        model = Variation
        fields = ('name', 'actual_stocks_var')
        labels = {
            'actual_stocks_var': 'No. of Stocks',
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(kwargs)
            
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['wholesaler', 'sold', 'id']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        