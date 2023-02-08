from django.db import models
from django.contrib.auth.models import User
from wholesalers.models import Wholesaler


class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.SET_NULL, related_name='wholesaler', null=True)
    business_name = models.CharField(max_length=255)
    address = models.TextField()
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
