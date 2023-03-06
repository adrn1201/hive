from django.db import models
from django.contrib.auth.models import User
from wholesalers.models import Wholesaler


class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    wholesaler = models.ForeignKey(Wholesaler, on_delete=models.SET_NULL, related_name='retailers', null=True)
    business_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=False, blank=True)
    region = models.CharField(max_length=255, null=False, blank=True)
    city = models.CharField(max_length=255, null=False, blank=True)
    contact_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    retailer_image = models.ImageField(default='products/default.jpg', upload_to="products/")
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['created'] 
        
    
    @property
    def image_url(self):
        try:
            url = self.retailer_image.url
        except:
            url = ''
        return url

class RetailerLogs(models.Model):
    retailer = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.action)
