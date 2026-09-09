from rest_framework import serializers
from .models import HistoryEvent
class HistorySerializer(serializers.ModelSerializer):
 class Meta: model=HistoryEvent; fields=["id","action","event_type","status","related_object","metadata","created_at","updated_at"];read_only_fields=["id","created_at","updated_at"]
