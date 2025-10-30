from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Visit, Survey
from .serializers import VisitSerializer, SurveySerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related("apartment", "visitor").all().order_by("-visited_at")
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["apartment", "visitor"]
    search_fields = [
        "apartment__building__address",
        "apartment__number",
        "note",
    ]

    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.select_related("visit", "visit__apartment").all().order_by("-updated_at")
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "provider_satisfaction",
        "interested_services",
    ]
