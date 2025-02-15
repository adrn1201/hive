from django.db import models
from django.core.exceptions import ValidationError
import uuid
from wholesalers.models import Wholesaler
import random
import string

def positive_validator(value):
    if value < 0:
        raise ValidationError('Price must be a positive number.')
    
def nonzero_validator(value):
    if value == 0:
        raise ValidationError('Price must be more than 0.')
    
def min_positive_validator(value):
    if value < 0:
        raise ValidationError('Minimum Order must be a positive number.')
    
def min_nonzero_validator(value):
    if value == 0:
        raise ValidationError('Minimum Order must be more than 0.')
    
def stock_positive_validator(value):
    if value < 0:
        raise ValidationError('Stocks must be a positive number.')
    
def stock_nonzero_validator(value):
    if value == 0:
        raise ValidationError('Stocks Order must be more than 0.')
    
class Category(models.Model):
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    sold = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
        
    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = (
		(1, 'Yes'),
		(0, 'No'),
	)

    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') 
    product_name = models.CharField(max_length=200, unique=True)
    actual_stocks = models.IntegerField(default=0, null=True, blank=True, validators=[stock_positive_validator,stock_nonzero_validator],
                              error_messages={'invalid': 'Please enter a valid number.'})
    tempo_stocks = models.IntegerField(default=0, null=True, blank=True,)
    price = models.FloatField(validators=[positive_validator,nonzero_validator],
                              error_messages={'invalid': 'Please enter a valid price.'})
    with_variation = models.BooleanField(choices=STATUS)
    sold = models.IntegerField(default=0)
    description = models.TextField(max_length=200)
    min_orders = models.IntegerField(default=actual_stocks,validators=[min_positive_validator,min_nonzero_validator],
                              error_messages={'invalid': 'Please enter a valid number.'})
    product_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)
    analytics_date = models.DateField(null=True, blank=True)
    id = models.CharField(max_length=5, primary_key=True, unique=True)

    def save(self, *args, **kwargs):
        while not self.id:
            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

            if not Product.objects.filter(id=random_id).exists():
                self.id = random_id

        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-created']
         
    def __str__(self):
        return self.product_name
    
    
    @property
    def product_sales(self):
        return self.price * self.sold
    

class Variation(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    actual_stocks_var = models.IntegerField(default=0)
    tempo_stocks_var = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    analytics_date = models.DateField(null=True, blank=True)
    id = models.CharField(max_length=5, primary_key=True, unique=True)

    def save(self, *args, **kwargs):
        while not self.id:
            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

            if not Variation.objects.filter(id=random_id).exists():
                self.id = random_id

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Sizes'
        ordering = ['created']
         
    def __str__(self):
        return self.name
    
