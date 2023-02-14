from django.db import models
from wholesalers.models import Wholesaler
from retailers.models import Retailer
from products.models import Inventory
import uuid
from django.contrib.auth.models import User


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('confirmed', 'Confirmed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    reference_number = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    business_name = models.CharField(max_length=255)
    total_paid = models.FloatField()
    mode_of_payment = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    is_received = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Inventory,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)