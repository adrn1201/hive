from django.db import models
from django.contrib.auth.models import User
import uuid
from products.models import Product, Variation


class Cart_DB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="products_cart")
    variation_id = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, related_name="variations")
    qty = models.IntegerField()
    subtotal = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['created']
    

