from rest_framework import serializers
from .models import ShortURL, ClickEvent

class ShortURLSerializer(serializers.ModelSerializer):
    """Converts ShortURL model to JSON format"""
    
    class Meta:
        model = ShortURL
        fields = ['short_code', 'original_url', 'total_clicks', 'created_at']

class ClickEventSerializer(serializers.ModelSerializer):
    """Converts ClickEvent model to JSON format"""
    
    class Meta:
        model = ClickEvent
        fields = ['clicked_at', 'device_type', 'country', 'ip_address']