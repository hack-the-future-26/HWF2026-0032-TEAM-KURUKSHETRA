from django.db import models
from apps.core.models import SupabaseUser,TimestampedModel
class HistoryEvent(TimestampedModel):
 user=models.ForeignKey(SupabaseUser,on_delete=models.CASCADE,related_name="history_events"); action=models.CharField(max_length=120); event_type=models.CharField(max_length=60,db_index=True); status=models.CharField(max_length=30,db_index=True); related_object=models.CharField(max_length=200,blank=True); metadata=models.JSONField(default=dict,blank=True)
 class Meta: indexes=[models.Index(fields=["user","-created_at"])]
