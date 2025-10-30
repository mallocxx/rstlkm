from django.db import models
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    region = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Building(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="buildings")
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("city", "address")
        indexes = [
            models.Index(fields=["city"]),
        ]

    def __str__(self) -> str:
        return f"{self.address}, {self.city.name}"


class Apartment(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="apartments")
    number = models.CharField(max_length=20)
    floor = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("building", "number")
        indexes = [
            models.Index(fields=["building", "number"]),
        ]

    def __str__(self) -> str:
        return f"{self.building.address} — apt {self.number}"
