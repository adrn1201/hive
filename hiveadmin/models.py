from django.db import models
from django.contrib.auth.models import User
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save


class EmailTenant(models.Model):
    email = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    reference_number = models.CharField(max_length=120, blank=True)
    business_name = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        instance.reference_number= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Transaction)
