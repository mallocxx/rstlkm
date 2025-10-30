from rest_framework import serializers
from .models import City, Building, Apartment


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "region", "created_at"]


class BuildingSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        source="city", queryset=City.objects.all(), write_only=True
    )

    class Meta:
        model = Building
        fields = [
            "id",
            "city",
            "city_id",
            "address",
            "latitude",
            "longitude",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["created_by", "created_at"]


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ["id", "building", "number", "floor", "notes"]
