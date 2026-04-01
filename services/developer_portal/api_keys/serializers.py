from rest_framework import serializers
from .models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ["id", "key", "created_at", "active"]
        read_only_fields = ["id", "key", "created_at"]