from rest_framework import serializers
from .models import UserSettings
class SettingsSerializer(serializers.ModelSerializer):
 class Meta: model=UserSettings; fields=["full_name","job_title","notification_preferences","ai_preferences","updated_at"];read_only_fields=["updated_at"]
