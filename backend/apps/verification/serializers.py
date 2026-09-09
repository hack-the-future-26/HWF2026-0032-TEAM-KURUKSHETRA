from rest_framework import serializers
from .models import VerificationRequest,VerificationDocument,VerificationResult,AuditLog
class DocumentSerializer(serializers.ModelSerializer):
 class Meta: model=VerificationDocument;fields=["id","original_name","mime_type","size","sha256","created_at"]
class ResultSerializer(serializers.ModelSerializer):
 class Meta: model=VerificationResult;fields=["confidence","details","errors","verified_at"]
class VerificationSerializer(serializers.ModelSerializer):
 officer=serializers.EmailField(source="officer.email",read_only=True);documents=DocumentSerializer(many=True,read_only=True);result=ResultSerializer(read_only=True)
 class Meta: model=VerificationRequest;fields=["id","verification_id","bidder_name","document_type","status","source","requires_manual_review","officer","created_at","updated_at","documents","result"]
class CreateVerificationSerializer(serializers.ModelSerializer):
 class Meta: model=VerificationRequest;fields=["bidder_name","document_type"]
class AuditLogSerializer(serializers.ModelSerializer):
 user_email=serializers.EmailField(source="user.email",read_only=True)
 class Meta: model=AuditLog;fields=["id","user_email","action","resource","result","ip_address","metadata","created_at"]
