from rest_framework import serializers
from .models import ChangeLog

class ChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeLog
        fields = ["id", "entity_type", "entity_id", "changed_by", "changed_at", "diff"]
