from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import City, Building, Apartment
from .serializers import CitySerializer, BuildingSerializer, ApartmentSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().order_by("name")
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "region"]


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.select_related("city").all().order_by("address")
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["city"]
    search_fields = ["address"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.select_related("building", "building__city").all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["building"]
    search_fields = ["number"]
