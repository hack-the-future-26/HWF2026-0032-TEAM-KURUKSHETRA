import uuid
from django.conf import settings
from django.db import models
class VerificationRequest(models.Model):
 class Status(models.TextChoices): VERIFIED="VERIFIED";FAILED="FAILED";PENDING="PENDING";PARTIALLY_VERIFIED="PARTIALLY_VERIFIED";MANUAL_REVIEW="MANUAL_REVIEW";API_UNAVAILABLE="API_UNAVAILABLE";INVALID_DOCUMENT="INVALID_DOCUMENT"
 id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); verification_id=models.CharField(max_length=24,unique=True,editable=False); bidder_name=models.CharField(max_length=255,db_index=True);document_type=models.CharField(max_length=40,db_index=True);status=models.CharField(max_length=24,choices=Status.choices,default=Status.PENDING,db_index=True);source=models.CharField(max_length=40,default="MANUAL_VERIFICATION_REQUIRED");requires_manual_review=models.BooleanField(default=True);officer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="verifications");created_at=models.DateTimeField(auto_now_add=True,db_index=True);updated_at=models.DateTimeField(auto_now=True)
 def save(self,*args,**kwargs):
  if not self.verification_id:self.verification_id="VER-"+uuid.uuid4().hex[:12].upper()
  return super().save(*args,**kwargs)
class VerificationDocument(models.Model):
 request=models.ForeignKey(VerificationRequest,on_delete=models.CASCADE,related_name="documents");file=models.FileField(upload_to="verification/%Y/%m/%d/");original_name=models.CharField(max_length=255);mime_type=models.CharField(max_length=100);size=models.PositiveIntegerField();sha256=models.CharField(max_length=64);created_at=models.DateTimeField(auto_now_add=True)
class VerificationResult(models.Model):
 request=models.OneToOneField(VerificationRequest,on_delete=models.CASCADE,related_name="result");confidence=models.DecimalField(max_digits=4,decimal_places=3,null=True,blank=True);details=models.JSONField(default=dict,blank=True);errors=models.JSONField(default=list,blank=True);verified_at=models.DateTimeField(null=True,blank=True);created_at=models.DateTimeField(auto_now_add=True)
class GovernmentAPIProvider(models.Model):
 name=models.CharField(max_length=80,unique=True);configured=models.BooleanField(default=False);status=models.CharField(max_length=30,default="MANUAL_VERIFICATION_REQUIRED");updated_at=models.DateTimeField(auto_now=True)
class AuditLog(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,null=True,blank=True);action=models.CharField(max_length=100,db_index=True);resource=models.CharField(max_length=100);result=models.CharField(max_length=30,default="SUCCESS");ip_address=models.GenericIPAddressField(null=True,blank=True);metadata=models.JSONField(default=dict,blank=True);created_at=models.DateTimeField(auto_now_add=True,db_index=True)
 class Meta: indexes=[models.Index(fields=["-created_at","action"])]
