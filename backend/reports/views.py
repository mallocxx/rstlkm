from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import ReportRequest
from .serializers import ReportRequestSerializer
from django.http import FileResponse
from django.conf import settings
import os, tempfile
from openpyxl import Workbook
from django.utils.timezone import now
from surveys.models import Survey, Visit
from locations.models import City, Building, Apartment

class ReportRequestViewSet(viewsets.ModelViewSet):
    queryset = ReportRequest.objects.all().order_by('-created_at')
    serializer_class = ReportRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate XLSX report based on filter payload; returns download url"""
        filters = request.data.get('filters', {})
        file_name = f"report_{int(now().timestamp())}.xlsx"
        tmp_path = os.path.join(settings.BASE_DIR, 'staticfiles', file_name)
        wb = Workbook()
        ws = wb.active
        ws.append(["Город", "Дом", "Квартира", "Дата визита", "Портрет", "Услуги (текущ)", "Услуги (интерес)", "Удовлетворенность", "Телефон", "Цена", "Комментарий"])

        qs = Survey.objects.all().select_related("visit","visit__apartment","visit__apartment__building","visit__apartment__building__city")
        # Apply filters
        if 'city' in filters:
            qs = qs.filter(visit__apartment__building__city_id=filters['city'])
        if 'building' in filters:
            qs = qs.filter(visit__apartment__building_id=filters['building'])
        if 'provider_satisfaction' in filters:
            qs = qs.filter(provider_satisfaction=filters['provider_satisfaction'])
        if 'interested_service' in filters:
            qs = qs.filter(interested_services__contains=[filters['interested_service']])
        if 'date_from' in filters:
            qs = qs.filter(visit__visited_at__gte=filters['date_from'])
        if 'date_to' in filters:
            qs = qs.filter(visit__visited_at__lte=filters['date_to'])
        for s in qs:
            ws.append([
                s.visit.apartment.building.city.name,
                s.visit.apartment.building.address,
                s.visit.apartment.number,
                s.visit.visited_at.strftime("%Y-%m-%d %H:%M"),
                s.client_profile,
                ", ".join(s.services_current or []),
                ", ".join(s.interested_services or []),
                s.provider_satisfaction,
                s.contact_phone,
                s.fair_price,
                s.comment,
            ])
        wb.save(tmp_path)
        rep = ReportRequest.objects.create(
            requested_by=request.user,
            filters=filters,
            file_path=file_name,
            status="done",
        )
        return Response({"id": rep.id, "file": f"/static/{file_name}"})

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        rep = self.get_object()
        path = os.path.join(settings.BASE_DIR, 'staticfiles', rep.file_path)
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=rep.file_path)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def stats_summary(request):
    city_id = request.query_params.get('city')
    # фильтрация по городу, если указано
    surqs = Survey.objects.all()
    if city_id:
        surqs = surqs.filter(visit__apartment__building__city_id=city_id)
    total = surqs.count()
    satisf = {}
    interest = {}
    for s in surqs:
        satisf[s.provider_satisfaction or ''] = satisf.get(s.provider_satisfaction or '', 0) + 1
        for intr in (s.interested_services or []):
            interest[intr] = interest.get(intr, 0) + 1
    # динамика по датам
    by_day = {}
    for s in surqs:
        d = s.visit.visited_at.date().isoformat()
        by_day[d] = by_day.get(d, 0) + 1
    return Response({
        "total": total, "by_satisfaction": satisf,
        "by_interest": interest,
        "by_day": sorted(by_day.items()),
    })
