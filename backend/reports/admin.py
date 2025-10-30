from django.contrib import admin
from .models import ReportRequest

@admin.register(ReportRequest)
class ReportRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "requested_by", "status", "file_path", "created_at")
    list_filter = ("status",)
