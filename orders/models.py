from django.db import models
from wholesalers.models import Wholesaler
from products.models import Product, Variation
import uuid
from django.contrib.auth.models import User


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    reference_number = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    business_name = models.CharField(max_length=255)
    address =  models.CharField(max_length=255, null=True, blank=True)
    total_paid = models.FloatField()
    mode_of_payment = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    is_received = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


