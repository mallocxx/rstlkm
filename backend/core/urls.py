from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from locations.views import CityViewSet, BuildingViewSet, ApartmentViewSet
from surveys.views import VisitViewSet, SurveyViewSet
from reports.views import ReportRequestViewSet, stats_summary

router = DefaultRouter()
router.register(r"cities", CityViewSet, basename="city")
router.register(r"buildings", BuildingViewSet, basename="building")
router.register(r"apartments", ApartmentViewSet, basename="apartment")
router.register(r"visits", VisitViewSet, basename="visit")
router.register(r"surveys", SurveyViewSet, basename="survey")
router.register(r"reports", ReportRequestViewSet, basename="report")

urlpatterns = [
    path("", lambda request: redirect("/api/docs/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/health/", lambda request: JsonResponse({"status": "ok"})),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
    path("api/reports/stats_summary/", stats_summary, name="stats-summary"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
