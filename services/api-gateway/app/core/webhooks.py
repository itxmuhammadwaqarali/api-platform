# Simulated for now; later connect to Django DB
from typing import List

def get_webhooks_for_event(event_name: str) -> List[str]:
    """
    Returns a list of webhook URLs for a specific event
    """
    # Example hard-coded, can query Django Webhook model later
    webhooks = {
        "rate_limit_exceeded": ["https://webhook.site/your-test-url"],
        "api_key_created": ["https://webhook.site/another-url"],
    }
    return webhooks.get(event_name, [])