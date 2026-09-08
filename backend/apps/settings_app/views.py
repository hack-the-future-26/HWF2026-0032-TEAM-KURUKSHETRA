from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserSettings
from .serializers import SettingsSerializer
from apps.officers.permissions import OfficerRequired
class SettingsView(APIView):
 permission_classes=[OfficerRequired]
 def get_object(self): return UserSettings.objects.order_by("id").first()
 def get(self,request):
  settings=self.get_object()
  if settings is None: return Response({"success":True,"data":{"full_name":"","job_title":"","notification_preferences":{},"ai_preferences":{},"updated_at":None}})
  return Response({"success":True,"data":SettingsSerializer(settings).data})
 def patch(self,request):
  settings=self.get_object()
  if settings is None: return Response({"success":False,"error":{"message":"No workspace settings record is available.","code":"SETTINGS_UNAVAILABLE"}},status=404)
  serializer=SettingsSerializer(settings,data=request.data,partial=True);serializer.is_valid(raise_exception=True);serializer.save();return Response({"success":True,"data":serializer.data})
