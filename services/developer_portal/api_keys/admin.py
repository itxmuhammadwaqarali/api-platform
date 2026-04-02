from django.contrib import admin
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'plan', 'active', 'created_at')
    list_filter = ('active', 'plan', 'created_at')
    search_fields = ('key', 'user__username', 'user__email')
    readonly_fields = ('id', 'created_at', 'key_display')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'plan', 'active', 'created_at')
        }),
        ('API Key', {
            'fields': ('key_display',),
            'description': 'The API key is auto-generated when you save. It will appear below after creation.'
        }),
    )

    def key_display(self, obj):
        """Display the generated key"""
        if obj.key:
            return f"<code style='background-color: #f0f0f0; padding: 10px; border-radius: 4px;'>{obj.key}</code>"
        return "Key will be generated on save"
    key_display.short_description = "Generated API Key"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')
