from django.core.management.base import BaseCommand
from plans.models import Plan

class Command(BaseCommand):
    help = 'Create default plans'

    def handle(self, *args, **options):
        # Create default plans if they don't exist
        plans_data = [
            {
                'name': 'free',
                'display_name': 'Free Plan',
                'description': 'Basic plan for getting started',
                'price_per_month': 0.00,
                'requests_per_minute': 10,
                'requests_per_hour': 100,
                'requests_per_day': 1000,
                'webhook_support': False,
                'priority_support': False,
                'custom_rate_limits': False,
            },
            {
                'name': 'basic',
                'display_name': 'Basic Plan',
                'description': 'Good for small applications',
                'price_per_month': 9.99,
                'requests_per_minute': 60,
                'requests_per_hour': 1000,
                'requests_per_day': 10000,
                'webhook_support': True,
                'priority_support': False,
                'custom_rate_limits': False,
            },
            {
                'name': 'pro',
                'display_name': 'Professional Plan',
                'description': 'For growing businesses',
                'price_per_month': 29.99,
                'requests_per_minute': 300,
                'requests_per_hour': 5000,
                'requests_per_day': 50000,
                'webhook_support': True,
                'priority_support': True,
                'custom_rate_limits': False,
            },
            {
                'name': 'enterprise',
                'display_name': 'Enterprise Plan',
                'description': 'For large-scale applications',
                'price_per_month': 99.99,
                'requests_per_minute': 1000,
                'requests_per_hour': 50000,
                'requests_per_day': 500000,
                'webhook_support': True,
                'priority_support': True,
                'custom_rate_limits': True,
            },
        ]

        for plan_data in plans_data:
            plan, created = Plan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created plan "{plan.display_name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan "{plan.display_name}" already exists')
                )
