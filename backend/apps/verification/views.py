import hashlib
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VerificationRequest,VerificationDocument,AuditLog,GovernmentAPIProvider
from .serializers import VerificationSerializer,CreateVerificationSerializer,AuditLogSerializer
from .services import run_verification
from apps.officers.permissions import OfficerRequired,SuperAdminRequired
def log(request,action,resource,metadata=None): AuditLog.objects.create(user=request.user,action=action,resource=resource,ip_address=request.META.get("REMOTE_ADDR") or None,metadata=metadata or {})
class VerificationListCreate(APIView):
 permission_classes=[OfficerRequired]
 def get(self,request):
  qs=VerificationRequest.objects.select_related("officer","result").prefetch_related("documents").order_by("-created_at")
  if request.user.officer_profile.role!="SUPER_ADMIN":qs=qs.filter(officer=request.user)
  for field in ("status","document_type"):
   if request.query_params.get(field):qs=qs.filter(**{field:request.query_params[field]})
  if request.query_params.get("q"):qs=qs.filter(bidder_name__icontains=request.query_params["q"])
  return Response({"success":True,"data":VerificationSerializer(qs[:100],many=True).data})
 def post(self,request):
  s=CreateVerificationSerializer(data=request.data);s.is_valid(raise_exception=True);item=s.save(officer=request.user);log(request,"VERIFICATION_REQUESTED",item.verification_id);return Response({"success":True,"data":VerificationSerializer(item).data},status=201)
class VerificationDetail(APIView):
 permission_classes=[OfficerRequired]
 def get_object(self,request,pk):
  try:item=VerificationRequest.objects.select_related("officer","result").prefetch_related("documents").get(pk=pk)
  except VerificationRequest.DoesNotExist:return None
  return item if request.user.officer_profile.role=="SUPER_ADMIN" or item.officer_id==request.user.id else False
 def get(self,request,pk):
  item=self.get_object(request,pk)
  if item is None:return Response({"success":False,"error":{"message":"Not found.","code":"NOT_FOUND"}},status=404)
  if item is False:return Response({"success":False,"error":{"message":"Forbidden.","code":"FORBIDDEN"}},status=403)
  return Response({"success":True,"data":VerificationSerializer(item).data})
 def post(self,request,pk):
  item=self.get_object(request,pk)
  if not item:return Response({"success":False,"error":{"message":"Not found or forbidden.","code":"NOT_FOUND"}},status=404)
  run_verification(item);log(request,"VERIFICATION_COMPLETED",item.verification_id,{"status":item.status});return Response({"success":True,"data":VerificationSerializer(item).data})
class UploadView(APIView):
 permission_classes=[OfficerRequired]
 def post(self,request,pk):
  try:item=VerificationRequest.objects.get(pk=pk,officer=request.user) if request.user.officer_profile.role!="SUPER_ADMIN" else VerificationRequest.objects.get(pk=pk)
  except VerificationRequest.DoesNotExist:return Response({"success":False,"error":{"message":"Not found.","code":"NOT_FOUND"}},status=404)
  f=request.FILES.get("file"); allowed={"application/pdf","image/jpeg","image/png"}
  if not f or f.content_type not in allowed or f.size>10*1024*1024:return Response({"success":False,"error":{"message":"Upload a PDF, JPG, JPEG, or PNG under 10 MB.","code":"INVALID_DOCUMENT"}},status=422)
  digest=hashlib.sha256(f.read()).hexdigest();f.seek(0);doc=VerificationDocument.objects.create(request=item,file=f,original_name=Path(f.name).name,mime_type=f.content_type,size=f.size,sha256=digest);log(request,"DOCUMENT_UPLOADED",item.verification_id,{"document":doc.original_name});return Response({"success":True,"data":{"id":doc.id,"name":doc.original_name}},status=201)
class AuditLogView(APIView):
 permission_classes=[SuperAdminRequired]
 def get(self,request):return Response({"success":True,"data":AuditLogSerializer(AuditLog.objects.select_related("user").order_by("-created_at")[:200],many=True).data})
class ProviderStatusView(APIView):
 permission_classes=[OfficerRequired]
 def get(self,request):return Response({"success":True,"data":[{"name":n,"status":"MANUAL_VERIFICATION_REQUIRED","configured":False} for n in ["GST","Udyam/MSME","PAN","EPFO","ESIC","Startup India","NSIC","DigiLocker","Blacklist"]]})
