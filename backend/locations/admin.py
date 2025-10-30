from django.contrib import admin
from .models import City, Building, Apartment


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "created_at")
    search_fields = ("name", "region")


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "city", "latitude", "longitude", "created_at")
    list_filter = ("city",)
    search_fields = ("address",)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "building", "number", "floor")
    list_filter = ("building",)
    search_fields = ("number",)
