from rest_framework import generics, permissions
from .models import APIKey
from .serializers import APIKeySerializer
import secrets

class APIKeyListCreateView(generics.ListCreateAPIView):
    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Generate a secure random API key
        api_key = secrets.token_urlsafe(32)
        serializer.save(user=self.request.user, key=api_key)