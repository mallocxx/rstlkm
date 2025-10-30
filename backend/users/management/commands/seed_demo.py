from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from locations.models import City, Building, Apartment


class Command(BaseCommand):
	help = "Seed demo users and sample data"

	def handle(self, *args, **options):
		# Users
		if not User.objects.filter(username="admin").exists():
			User.objects.create_superuser("admin", "admin@example.com", "admin123")
			self.stdout.write(self.style.SUCCESS("Created superuser admin/admin123"))
		else:
			self.stdout.write("Superuser admin exists")

		if not User.objects.filter(username="engineer").exists():
			User.objects.create_user("engineer", password="engineer123")
			self.stdout.write(self.style.SUCCESS("Created engineer engineer/engineer123"))
		else:
			self.stdout.write("Engineer user exists")

		# Cities
		mkc, _ = City.objects.get_or_create(name="Махачкала", defaults={"region": "РД"})
		kpc, _ = City.objects.get_or_create(name="Каспийск", defaults={"region": "РД"})

		# Buildings
		b1, _ = Building.objects.get_or_create(city=mkc, address="ул. Ленина, 10", defaults={"latitude": 42.9845, "longitude": 47.5040})
		b2, _ = Building.objects.get_or_create(city=kpc, address="пр. Набережный, 5", defaults={"latitude": 42.8820, "longitude": 47.6390})

		# Apartments
		for num in ["1", "2", "3", "10", "15"]:
			Apartment.objects.get_or_create(building=b1, number=num)
			Apartment.objects.get_or_create(building=b2, number=num)

		self.stdout.write(self.style.SUCCESS("Demo data seeded."))
