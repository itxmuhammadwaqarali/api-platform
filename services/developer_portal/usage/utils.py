from .models import APIUsage

def log_api_usage(api_key, endpoint, method):
    APIUsage.objects.create(api_key=api_key, endpoint=endpoint, method=method)