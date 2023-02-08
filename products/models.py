from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    

    class Meta:
        verbose_name_plural = 'Categories'
        
        
    def __str__(self):
        return self.name
    
    
class Inventory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True) 
    product_name = models.CharField(max_length=200, null=True, blank=True)
    actual_quantity = models.IntegerField(default=0, null=True, blank=True)
    tempo_quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    with_size = models.BooleanField(default=False, null=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_orders = models.IntegerField(null=True, default=0, blank=True)
    product_image = models.ImageField(null=True, blank=True, default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    
    class Meta:
        verbose_name_plural = 'Inventories'
         
    def __str__(self):
        return self.product_name


    
