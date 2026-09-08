from django.contrib.auth import authenticate,get_user_model,login,logout
from django.middleware.csrf import get_token
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import OfficerProfile,OfficerInvitation
from .permissions import OfficerRequired,SuperAdminRequired
from .serializers import LoginSerializer,RegistrationSerializer,InvitationSerializer,OfficerSerializer
from .throttles import LoginRateThrottle
User=get_user_model()
def record(user,action,metadata=None):
    from apps.verification.models import AuditLog
    AuditLog.objects.create(user=user,action=action,resource="OFFICER",metadata=metadata or {})
class CsrfView(APIView):
 permission_classes=[AllowAny]
 def get(self,request): return Response({"success":True,"data":{"csrfToken":get_token(request)}})
class LoginView(APIView):
 permission_classes=[AllowAny]
 throttle_classes=[LoginRateThrottle]
 def post(self,request):
  s=LoginSerializer(data=request.data);s.is_valid(raise_exception=True); user=authenticate(request,username=s.validated_data["email"],password=s.validated_data["password"])
  if not user or not user.is_active or not hasattr(user,"officer_profile") or not user.officer_profile.is_active:
   return Response({"success":False,"error":{"message":"Invalid credentials or unauthorized officer account.","code":"INVALID_LOGIN"}},status=401)
  login(request,user); record(user,"LOGIN",{"ip":request.META.get("REMOTE_ADDR","")}); return Response({"success":True,"data":{"email":user.email,"role":user.officer_profile.role}})
class LogoutView(APIView):
 permission_classes=[OfficerRequired]
 def post(self,request): record(request.user,"LOGOUT"); logout(request); return Response({"success":True,"data":None})
class MeView(APIView):
 permission_classes=[OfficerRequired]
 def get(self,request): return Response({"success":True,"data":{"email":request.user.email,"role":request.user.officer_profile.role,"is_active":request.user.officer_profile.is_active}})
class RegisterView(APIView):
 permission_classes=[AllowAny]
 def post(self,request):
  s=RegistrationSerializer(data=request.data);s.is_valid(raise_exception=True)
  try: invite=OfficerInvitation.objects.get(token=s.validated_data["token"])
  except OfficerInvitation.DoesNotExist: return Response({"success":False,"error":{"message":"The invitation is invalid or expired.","code":"INVALID_INVITATION"}},status=422)
  if not invite.valid:return Response({"success":False,"error":{"message":"The invitation is invalid or expired.","code":"INVALID_INVITATION"}},status=422)
  if invite.email.lower()!=s.validated_data["email"].lower():return Response({"success":False,"error":{"message":"This email does not match the invitation.","code":"INVALID_INVITATION"}},status=422)
  user=User.objects.filter(email__iexact=invite.email).first()
  if user:return Response({"success":False,"error":{"message":"Account registration cannot be completed.","code":"CONFLICT"}},status=409)
  user=User.objects.create_user(username=invite.email,email=invite.email,password=s.validated_data["password"],is_active=True)
  OfficerProfile.objects.create(user=user,is_active=True);invite.accepted_at=timezone.now();invite.save(update_fields=["accepted_at"]);record(user,"OFFICER_REGISTERED");return Response({"success":True,"data":{"email":user.email}},status=201)
class OfficerListView(APIView):
 permission_classes=[SuperAdminRequired]
 def get(self,request): return Response({"success":True,"data":OfficerSerializer(OfficerProfile.objects.select_related("user").order_by("-created_at"),many=True).data})
class InvitationView(APIView):
 permission_classes=[SuperAdminRequired]
 def post(self,request):
  s=InvitationSerializer(data=request.data);s.is_valid(raise_exception=True);email=s.validated_data["email"].lower()
  if User.objects.filter(email__iexact=email).exists() or OfficerInvitation.objects.filter(email__iexact=email,accepted_at__isnull=True,revoked_at__isnull=True,expires_at__gt=timezone.now()).exists():return Response({"success":False,"error":{"message":"An officer or active invitation already exists.","code":"CONFLICT"}},status=409)
  invite=OfficerInvitation.objects.create(email=email,created_by=request.user);record(request.user,"OFFICER_INVITED",{"email":email});return Response({"success":True,"data":InvitationSerializer(invite).data},status=201)
class OfficerActionView(APIView):
 permission_classes=[SuperAdminRequired]
 def post(self,request,pk,action):
  try: profile=OfficerProfile.objects.select_related("user").get(pk=pk)
  except OfficerProfile.DoesNotExist:return Response({"success":False,"error":{"message":"Officer not found.","code":"NOT_FOUND"}},status=404)
  if profile.role==OfficerProfile.Role.SUPER_ADMIN:return Response({"success":False,"error":{"message":"The official administrator cannot be modified here.","code":"FORBIDDEN"}},status=403)
  if action=="activate": profile.is_active=True;profile.user.is_active=True
  elif action in ("deactivate","revoke"): profile.is_active=False;profile.user.is_active=False
  else:return Response({"success":False,"error":{"message":"Invalid officer action.","code":"VALIDATION_ERROR"}},status=422)
  profile.save();profile.user.save(update_fields=["is_active"]);record(request.user,"OFFICER_"+action.upper(),{"email":profile.user.email});return Response({"success":True,"data":OfficerSerializer(profile).data})
