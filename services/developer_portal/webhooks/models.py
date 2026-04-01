from django.db import models

class Webhook(models.Model):
    url = models.URLField()
    event_type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} -> {self.url}"