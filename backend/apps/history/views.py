from rest_framework import mixins,viewsets
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from .models import HistoryEvent
from .serializers import HistorySerializer
from apps.officers.permissions import OfficerRequired
class HistoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
 permission_classes=[OfficerRequired]
 serializer_class=HistorySerializer; search_fields=["action","event_type","status","related_object"]; ordering_fields=["created_at","action","status"]; filterset_fields=["status","event_type"]
 def get_queryset(self):
  qs=HistoryEvent.objects.all()
  start=parse_date(self.request.query_params.get("date_from","") or "")
  end=parse_date(self.request.query_params.get("date_to","") or "")
  if start: qs=qs.filter(created_at__date__gte=start)
  if end: qs=qs.filter(created_at__date__lte=end)
  return qs.order_by("-created_at")
 def retrieve(self,request,*args,**kwargs): return Response({"success":True,"data":self.get_serializer(self.get_object()).data})
 def destroy(self,request,*args,**kwargs):
  instance=self.get_object(); instance.delete(); return Response({"success":True,"data":None},status=204)
