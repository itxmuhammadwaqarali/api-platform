from django.core.management.base import BaseCommand
from api_keys.models import APIKey
from plans.models import Plan

class Command(BaseCommand):
    help = 'Assign free plan to API keys that don\'t have a plan'

    def handle(self, *args, **options):
        try:
            free_plan = Plan.objects.get(name='free')
        except Plan.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Free plan does not exist. Run "python manage.py create_default_plans" first.')
            )
            return

        # Get API keys without plans
        keys_without_plan = APIKey.objects.filter(plan__isnull=True)
        count = keys_without_plan.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('All API keys already have plans assigned.')
            )
            return

        # Assign free plan to keys without plans
        keys_without_plan.update(plan=free_plan)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully assigned free plan to {count} API key(s).')
        )
