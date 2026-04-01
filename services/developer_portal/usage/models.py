from django.db import models
from django.conf import settings

class APIUsage(models.Model):
    api_key = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)