from django.contrib import admin
from .models import ShortURL, ClickEvent

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'user', 'original_url', 'total_clicks', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('short_code', 'original_url')
    readonly_fields = ('short_code', 'created_at', 'total_clicks')

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'device_type', 'clicked_at', 'ip_address')
    list_filter = ('device_type', 'clicked_at')
    search_fields = ('short_url__short_code', 'ip_address')
    readonly_fields = ('clicked_at',)