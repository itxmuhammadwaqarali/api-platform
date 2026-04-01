import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(BASE_DIR, "services/developer_portal"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "developer_portal.settings")

try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {e}")