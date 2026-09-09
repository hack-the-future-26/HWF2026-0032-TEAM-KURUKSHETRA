from django.db import models
from apps.core.models import SupabaseUser,TimestampedModel
class AuditRecord(TimestampedModel):
 user=models.ForeignKey(SupabaseUser,on_delete=models.CASCADE,related_name="audit_records"); action=models.CharField(max_length=120); event_type=models.CharField(max_length=60,db_index=True); status=models.CharField(max_length=30,db_index=True); result=models.CharField(max_length=300,blank=True); description=models.TextField(); metadata=models.JSONField(default=dict,blank=True)
 class Meta: indexes=[models.Index(fields=["user","-created_at"]),models.Index(fields=["status","-created_at"])]
