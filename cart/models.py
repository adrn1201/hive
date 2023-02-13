from django.db import models
from django.contrib.auth.models import User
import uuid


class Cart_DB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.UUIDField(default=uuid.uuid4, editable=False)
    size = models.CharField(max_length=255, null=True, blank=True)
    qty = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.product_id)
