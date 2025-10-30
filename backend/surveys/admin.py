from django.contrib import admin
from .models import Visit, Survey


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("id", "apartment", "visitor", "visited_at", "latitude", "longitude")
    list_filter = ("visited_at",)
    search_fields = ("apartment__building__address", "apartment__number")


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("id", "visit", "provider_satisfaction", "contact_phone", "updated_at")
    list_filter = ("provider_satisfaction",)
