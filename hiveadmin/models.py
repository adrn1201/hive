from django.db import models
from django.contrib.auth.models import User

class EmailTenant(models.Model):
    email = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
