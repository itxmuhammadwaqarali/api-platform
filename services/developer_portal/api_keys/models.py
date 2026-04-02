import uuid
import secrets
from django.db import models
from django.contrib.auth.models import User
from plans.models import Plan

class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=128, unique=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True, related_name="api_keys")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-generate API key if it's not provided
        if not self.key:
            self.key = secrets.token_urlsafe(32)
        
        # Assign free plan if not provided
        if not self.plan:
            try:
                free_plan = Plan.objects.get(name='free')
                self.plan = free_plan
            except Plan.DoesNotExist:
                pass  # Plan doesn't exist, will be None
        
        super().save(*args, **kwargs)

    def __str__(self):
        plan_name = self.plan.display_name if self.plan else "No Plan"
        return f"{self.user.username} - {self.key} ({plan_name})"
