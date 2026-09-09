from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import OfficerProfile,OfficerInvitation
User=get_user_model()
class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(); password=serializers.CharField(write_only=True,trim_whitespace=False)
class InvitationSerializer(serializers.ModelSerializer):
    class Meta: model=OfficerInvitation; fields=["id","email","token","expires_at","accepted_at","revoked_at","created_at"]; read_only_fields=["id","token","accepted_at","revoked_at","created_at"]
class OfficerSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(source="user.email",read_only=True); last_login=serializers.DateTimeField(source="user.last_login",read_only=True)
    class Meta: model=OfficerProfile; fields=["id","email","role","is_active","created_at","last_login"]
class RegistrationSerializer(serializers.Serializer):
    token=serializers.CharField(); email=serializers.EmailField(); password=serializers.CharField(min_length=12,write_only=True,trim_whitespace=False)
    password_confirmation=serializers.CharField(min_length=12,write_only=True,trim_whitespace=False)
    def validate(self,attrs):
        if attrs["password"]!=attrs["password_confirmation"]:
            raise serializers.ValidationError({"password_confirmation":"Passwords do not match."})
        return attrs
