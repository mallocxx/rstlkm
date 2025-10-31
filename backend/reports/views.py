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
from collections import defaultdict

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
    surqs = Survey.objects.all().select_related('visit', 'visit__apartment', 'visit__apartment__building', 'visit__apartment__building__city')
    if city_id:
        surqs = surqs.filter(visit__apartment__building__city_id=city_id)
    
    total = surqs.count()
    satisf = {}
    interest = {}
    
    # 1. Количество объектов по статусам (используем статусы зданий на основе активности)
    buildings = Building.objects.all().select_related('city')
    if city_id:
        buildings = buildings.filter(city_id=city_id)
    
    building_statuses = defaultdict(int)
    for b in buildings:
        visits_count = Visit.objects.filter(apartment__building=b).count()
        surveys_count = Survey.objects.filter(visit__apartment__building=b).count()
        
        if visits_count == 0:
            building_statuses['Не активен'] += 1
        elif surveys_count == 0:
            building_statuses['На рассмотрении'] += 1
        elif surveys_count == visits_count:
            building_statuses['Завершён'] += 1
        else:
            building_statuses['Активен'] += 1
    
    # 2. Уровень удовлетворённости провайдерами (группируем по типам услуг как провайдерам)
    provider_satisfaction = defaultdict(list)
    for s in surqs:
        if s.provider_satisfaction:
            # Преобразуем удовлетворённость в числовое значение
            sat_val = None
            if s.provider_satisfaction in ['1', '2', '3', '4', '5']:
                sat_val = float(s.provider_satisfaction)
            elif s.provider_satisfaction == 'SAT':
                sat_val = 4.5
            elif s.provider_satisfaction == 'UNSAT':
                sat_val = 2.0
            
            if sat_val is not None:
                # Используем текущие услуги как провайдеры
                providers = s.services_current or []
                if providers:
                    for prov in providers:
                        provider_satisfaction[prov].append(sat_val)
                else:
                    provider_satisfaction['Без услуг'].append(sat_val)
    
    # Вычисляем средние значения для провайдеров
    provider_avg = {}
    for prov, values in provider_satisfaction.items():
        if values:
            provider_avg[prov] = round(sum(values) / len(values), 2)
    
    # 3. Доля потенциальных клиентов по районам (используем города как районы)
    district_clients = defaultdict(int)
    for s in surqs:
        city = s.visit.apartment.building.city
        district_name = city.region or city.name
        district_clients[district_name] += 1
    
    # 4. Динамика визитов по датам
    by_day = {}
    for s in surqs:
        d = s.visit.visited_at.date().isoformat()
        by_day[d] = by_day.get(d, 0) + 1
    
    # Старые данные для обратной совместимости
    for s in surqs:
        satisf[s.provider_satisfaction or ''] = satisf.get(s.provider_satisfaction or '', 0) + 1
        for intr in (s.interested_services or []):
            interest[intr] = interest.get(intr, 0) + 1
    
    return Response({
        "total": total,
        "by_satisfaction": satisf,
        "by_interest": interest,
        "by_day": sorted(by_day.items()),
        # Новые данные
        "by_status": dict(building_statuses),
        "by_provider_satisfaction": provider_avg,
        "by_district": dict(district_clients),
    })
