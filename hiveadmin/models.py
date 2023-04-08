from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
import random
import string
import datetime
from django.utils import timezone



def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    reference_number= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(reference_number=reference_number).exists()
    if qs_exists:   
        return unique_order_id_generator(instance)
    return reference_number


class EmailTenant(models.Model):
    email = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

class Transaction(models.Model):
    reference_number = models.CharField(max_length=120, blank=True)
    business_name = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    expires = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    @property
    def is_expiring_soon(self):
        if not self.expires:
            return False
        today = timezone.now().date()
        # Define a threshold for what is considered "near" expiry
        expiry_threshold = 7  # days
        return (self.expires - today).days <= expiry_threshold
    

def pre_save_set_expires(sender, instance, *args, **kwargs):
    if instance.expires:
        # Convert Unix timestamp to datetime object
        expires_datetime = datetime.datetime.fromtimestamp(instance.expires)
        # Extract the date part of the datetime object
        expires_date = expires_datetime.date()
        # Set the expires field to the date object
        instance.expires = expires_date

pre_save.connect(pre_save_set_expires, sender=Transaction)

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.reference_number:
        instance.reference_number= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Transaction)

class AdminWholesalerLogs(models.Model):
    wholesaler = models.CharField(max_length=255) 
    domain = models.CharField(max_length=255) 
    action = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True) 
    
    
    def __str__(self):
        return str(self.action)
    

class AdminRetailerLogs(models.Model):
    wholesaler = models.CharField(max_length=255)
    retailer = models.CharField(max_length=255) 
    domain = models.CharField(max_length=255) 
    action = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True) 
    
    
    def __str__(self):
        return str(self.action)
 