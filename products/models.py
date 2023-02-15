from django.db import models
from django.core.exceptions import ValidationError
import uuid
from wholesalers.models import Wholesaler


class Category(models.Model):
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    

    class Meta:
        verbose_name_plural = 'Categories'
        
        
    def __str__(self):
        return self.name
    
    
class Inventory(models.Model):
    STATUS = (
		('True', 'Yes'),
		('False', 'No'),
	)

    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories') 
    product_name = models.CharField(max_length=200)
    actual_quantity = models.IntegerField(default=0)
    tempo_quantity = models.IntegerField(default=0)
    price = models.FloatField()
    with_size = models.BooleanField(default=False, choices=STATUS)
    size = models.CharField(max_length=200)
    description = models.TextField()
    min_orders = models.IntegerField(default=0)
    product_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    
    
    class Meta:
        verbose_name_plural = 'Inventories'
         
    def __str__(self):
        return self.product_name


    
