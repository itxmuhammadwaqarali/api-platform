from rest_framework import serializers
from .models import APIKey
from plans.models import Plan
import secrets

class APIKeySerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.display_name', read_only=True)
    plan_display = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = APIKey
        fields = ["id", "key", "plan", "plan_name", "plan_display", "created_at", "active"]
        read_only_fields = ["id", "key", "plan", "created_at", "plan_name", "plan_display"]

    def create(self, validated_data):
        # Generate a secure random API key
        api_key = secrets.token_urlsafe(32)

        # Get user from context
        user = self.context['request'].user

        # Assign free plan by default
        try:
            free_plan = Plan.objects.get(name='free')
        except Plan.DoesNotExist:
            # If no free plan exists, create one
            free_plan = Plan.objects.create(
                name='free',
                display_name='Free Plan',
                description='Basic plan for getting started',
                price_per_month=0.00,
                requests_per_minute=10,
                requests_per_hour=100,
                requests_per_day=1000,
                webhook_support=False,
                priority_support=False,
                custom_rate_limits=False,
            )

        # Create the API key with generated key, user, and default plan
        validated_data['key'] = api_key
        validated_data['user'] = user
        validated_data['plan'] = free_plan
        validated_data['active'] = True

        return super().create(validated_data)
