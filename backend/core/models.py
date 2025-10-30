from django.db import models
from django.contrib.auth import get_user_model

class ChangeLog(models.Model):
    entity_type = models.CharField(max_length=64)
    entity_id = models.IntegerField()
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    diff = models.JSONField(default=dict)

    class Meta:
        indexes = [models.Index(fields=["entity_type", "entity_id", "changed_at"]) ]

    def __str__(self):
        return f"{self.entity_type}#{self.entity_id} at {self.changed_at}"
