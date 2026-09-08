from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date
from .models import AuditRecord
from .serializers import AuditSerializer
from apps.officers.permissions import SuperAdminRequired
class AuditViewSet(ModelViewSet):
 permission_classes=[SuperAdminRequired]
 serializer_class=AuditSerializer; search_fields=["action","event_type","status","description","result"]; ordering_fields=["created_at","action","status"] ; filterset_fields=["status","event_type"]
 def get_queryset(self):
  qs=AuditRecord.objects.all()
  start=parse_date(self.request.query_params.get("date_from","") or "")
  end=parse_date(self.request.query_params.get("date_to","") or "")
  if start: qs=qs.filter(created_at__date__gte=start)
  if end: qs=qs.filter(created_at__date__lte=end)
  return qs.select_related("user").order_by("-created_at")
 def retrieve(self,request,*a,**k): return Response({"success":True,"data":self.get_serializer(self.get_object()).data})
 def create(self,request,*a,**k):
  serializer=self.get_serializer(data=request.data);serializer.is_valid(raise_exception=True);self.perform_create(serializer);return Response({"success":True,"data":serializer.data},status=status.HTTP_201_CREATED)
 def partial_update(self,request,*a,**k):
  serializer=self.get_serializer(self.get_object(),data=request.data,partial=True);serializer.is_valid(raise_exception=True);serializer.save();return Response({"success":True,"data":serializer.data})
 def destroy(self,request,*a,**k): self.get_object().delete();return Response({"success":True,"data":None},status=status.HTTP_204_NO_CONTENT)
