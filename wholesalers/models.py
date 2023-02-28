from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django_tenants.models import DomainMixin, TenantMixin

class Wholesaler(TenantMixin):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=False, blank=True)
    region = models.CharField(max_length=255, null=False, blank=True)
    city = models.CharField(max_length=255, null=False, blank=True)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    color = models.CharField(max_length=255, null=True, blank=True)
    wholesaler_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)
    
    auto_create_schema = True

    auto_drop_schema = True
    

class Domain(DomainMixin):
    pass




