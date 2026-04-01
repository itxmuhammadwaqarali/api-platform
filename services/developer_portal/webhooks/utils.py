from .models import Webhook

def get_webhooks_for_event(event_type):
    return Webhook.objects.filter(event_type=event_type, active=True)
