from django.db import models
from django.core.exceptions import ValidationError
import uuid
from wholesalers.models import Wholesaler
import random
import string

class Category(models.Model):
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    sold = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    
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
    product_name = models.CharField(max_length=200)
    actual_stocks = models.IntegerField(default=0, null=True, blank=True)
    tempo_stocks = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField()
    with_variation = models.BooleanField(choices=STATUS)
    sold = models.IntegerField(default=0)
    description = models.TextField(max_length=200)
    min_orders = models.IntegerField(default=actual_stocks)
    product_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_lenght=1000, primary_key=True, unique=True)
    
    
    class Meta:
        verbose_name_plural = 'Products'
         
    def __str__(self):
        return self.product_name
    
    
    @property
    def product_sales(self):
        return self.price * self.sold
    
def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    reference_number= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(reference_number=reference_number).exists()
    if qs_exists:   
        return unique_order_id_generator(instance)
    return reference_number


class Variation(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    actual_stocks_var = models.IntegerField(default=0)
    tempo_stocks_var = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
     
    class Meta:
        verbose_name_plural = 'Sizes'
        ordering = ['created']
         
    def __str__(self):
        return self.name