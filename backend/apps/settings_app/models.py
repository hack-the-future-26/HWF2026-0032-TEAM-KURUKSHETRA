from django.db import models
from apps.core.models import SupabaseUser,TimestampedModel
class UserSettings(TimestampedModel):
 user=models.OneToOneField(SupabaseUser,on_delete=models.CASCADE,related_name="settings"); full_name=models.CharField(max_length=160,blank=True); job_title=models.CharField(max_length=160,blank=True); notification_preferences=models.JSONField(default=dict); ai_preferences=models.JSONField(default=dict)
