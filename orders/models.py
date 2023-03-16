from django.db import models
from wholesalers.models import Wholesaler
from products.models import Product, Variation
import uuid
from django.contrib.auth.models import User
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=120, blank= True)
    business_name = models.CharField(max_length=255, null=True, blank=True)
    address =  models.CharField(max_length=255, null=True, blank=True)
    barangay = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, default="Zamboanga Peninsula", editable=False)
    city = models.CharField(max_length=255, default="Zamboanga City", editable=False)
    total_paid = models.FloatField()
    mode_of_payment = models.CharField(max_length=255)
    success = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    is_received = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    
    # class Meta: 
    #     ordering = ['-created']
    
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        instance.reference_number= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)


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


