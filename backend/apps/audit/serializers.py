from rest_framework import serializers
from .models import AuditRecord
class AuditSerializer(serializers.ModelSerializer):
 user_email=serializers.CharField(source="user.email",read_only=True)
 class Meta: model=AuditRecord; fields=["id","user_email","action","event_type","status","result","description","metadata","created_at","updated_at"]; read_only_fields=["id","user_email","created_at","updated_at"]
