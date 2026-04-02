import os
import sys
import django

# Path to the parent folder containing the Django project
GATEWAY_DIR = os.path.dirname(os.path.abspath(__file__))
DJANGO_PARENT_PATH = os.path.abspath(os.path.join(GATEWAY_DIR, "../../../developer_portal"))
print("Adding to path:", DJANGO_PARENT_PATH)  # Debug
sys.path.append(DJANGO_PARENT_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "developer_portal.settings")

try:
    django.setup()
except Exception as e:
    print("Django setup error:", e)
    raise
from api_keys.models import APIKey
from webhooks.models import Webhook
