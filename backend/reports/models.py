from django.db import models
from django.contrib.auth import get_user_model
import jsonfield

class ReportRequest(models.Model):
    requested_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    filters = jsonfield.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=32, default="pending")

    def __str__(self):
        return f"Report {self.id} by {self.requested_by}"
