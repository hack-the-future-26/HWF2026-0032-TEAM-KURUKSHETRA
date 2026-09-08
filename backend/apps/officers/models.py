import secrets
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

def invitation_token(): return secrets.token_urlsafe(32)
def invitation_expiry(): return timezone.now()+timedelta(days=7)
class OfficerProfile(models.Model):
    class Role(models.TextChoices): SUPER_ADMIN="SUPER_ADMIN"; OFFICER="OFFICER"
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="officer_profile")
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.OFFICER,db_index=True)
    is_active=models.BooleanField(default=False,db_index=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

class OfficerInvitation(models.Model):
    email=models.EmailField(unique=True); token=models.CharField(max_length=64,unique=True,default=invitation_token)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="officer_invitations")
    expires_at=models.DateTimeField(default=invitation_expiry); accepted_at=models.DateTimeField(null=True,blank=True)
    revoked_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    @property
    def valid(self): return not self.accepted_at and not self.revoked_at and self.expires_at>timezone.now()
