from rest_framework.views import APIView
from apps.officers.permissions import OfficerRequired
from rest_framework.response import Response
from rest_framework import serializers,status
from .services import analyze_bid,AIServiceError
class AnalyzeSerializer(serializers.Serializer):
 bidder=serializers.CharField(max_length=200); tender=serializers.CharField(max_length=300); score=serializers.IntegerField(min_value=0,max_value=100); findings=serializers.ListField(child=serializers.CharField(max_length=300),max_length=30)
class AnalyzeView(APIView):
 permission_classes=[OfficerRequired]
 def post(self,request):
  serializer=AnalyzeSerializer(data=request.data);serializer.is_valid(raise_exception=True)
  try: summary=analyze_bid(serializer.validated_data)
  except AIServiceError as e:return Response({"success":False,"error":{"message":str(e),"code":"AI_UNAVAILABLE"}},status=status.HTTP_503_SERVICE_UNAVAILABLE)
  return Response({"success":True,"data":{"summary":summary}})
