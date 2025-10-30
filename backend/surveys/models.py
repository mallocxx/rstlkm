from django.db import models
from django.contrib.auth import get_user_model
from locations.models import Apartment


class Visit(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="visits")
    visitor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_source = models.CharField(max_length=20, default="gps")  # gps/manual

    note = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["apartment", "visited_at"]),
        ]

    def __str__(self) -> str:
        return f"Visit {self.id} to {self.apartment}"


class Survey(models.Model):
    SERVICE_CHOICES = (
        ("INTERNET", "Internet"),
        ("TV", "Digital TV"),
        ("CCTV", "Video Surveillance"),
        ("NANNY", "Internet Nanny"),
    )
    SATISFACTION_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("SAT", "Satisfied"),
        ("UNSAT", "Unsatisfied"),
    )

    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name="survey")

    client_profile = models.CharField(max_length=255, blank=True)
    services_current = models.JSONField(default=list, blank=True)  # list of SERVICE_CHOICES keys
    provider_satisfaction = models.CharField(max_length=5, choices=SATISFACTION_CHOICES, blank=True)
    interested_services = models.JSONField(default=list, blank=True)  # list of SERVICE_CHOICES keys

    best_call_time = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    fair_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    comment = models.TextField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Survey for {self.visit}"
