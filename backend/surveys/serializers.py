from rest_framework import serializers
from .models import Visit, Survey


class SurveyInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            "id",
            "client_profile",
            "services_current",
            "provider_satisfaction",
            "interested_services",
            "best_call_time",
            "contact_phone",
            "fair_price",
            "comment",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]


class VisitSerializer(serializers.ModelSerializer):
    survey = SurveyInlineSerializer(read_only=True)
    class Meta:
        model = Visit
        fields = [
            "id",
            "apartment",
            "visitor",
            "visited_at",
            "latitude",
            "longitude",
            "location_source",
            "note",
            "survey",
        ]
        read_only_fields = ["visitor", "visited_at"]


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = [
            "id",
            "visit",
            "client_profile",
            "services_current",
            "provider_satisfaction",
            "interested_services",
            "best_call_time",
            "contact_phone",
            "fair_price",
            "comment",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
