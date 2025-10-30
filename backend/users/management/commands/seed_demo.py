from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from locations.models import City, Building, Apartment
from surveys.models import Visit, Survey
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Seed demo users and sample data"

    def handle(self, *args, **options):
        # Пользователи
        admin, _ = User.objects.get_or_create(username="admin", defaults={"is_superuser": True, "is_staff": True, "email": "admin@example.com"})
        admin.set_password("admin123")
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        admin.profile.role = 'admin'; admin.profile.save()
        self.stdout.write(self.style.SUCCESS("Superuser admin/admin123"))

        eng1, _ = User.objects.get_or_create(username="engineer", defaults={"is_staff": True, "email": "engineer@example.com"})
        eng1.set_password("engineer123")
        eng1.save()
        eng1.profile.role = 'engineer'; eng1.profile.save()

        eng2, _ = User.objects.get_or_create(username="engineer2", defaults={"is_staff": True, "email": "eng2@example.com"})
        eng2.set_password("eng2pass")
        eng2.save()
        eng2.profile.role = 'engineer'; eng2.profile.save()

        sv, _ = User.objects.get_or_create(username="supervisor", defaults={"is_staff": True, "email": "sv@example.com"})
        sv.set_password("sv123")
        sv.is_staff = True
        sv.save()
        sv.profile.role = 'supervisor'; sv.profile.save()
        
        # Города
        city_names = [
            ("Махачкала", "РД"),
            ("Каспийск", "РД"),
            ("Дербент", "РД"),
            ("Избербаш", "РД"),
            ("Хасавюрт", "РД"),
        ]
        cities = []
        for nm, region in city_names:
            city, _ = City.objects.get_or_create(name=nm, defaults={"region": region})
            cities.append(city)
        
        # Дома (buildings)
        from random import randint
        buildings = []
        adrs = [
            ("ул. Ленина, 10", 42.9845, 47.5040),
            ("ул. Горная, 22", 42.9870, 47.5080),
            ("пр. Набережный, 5", 42.8820, 47.6390),
            ("ул. Советская, 1", 42.0560, 48.2890),
        ]
        for i, city in enumerate(cities):
            for j in range(3):
                a = adrs[j % len(adrs)]
                addr = a[0] if j == 0 else a[0].replace(",", f", корп.{j}")
                b, _ = Building.objects.get_or_create(city=city, address=addr, defaults={"latitude": a[1]+i*0.01+j*0.001, "longitude": a[2]+i*0.01+j*0.001})
                buildings.append(b)
        
        # Квартиры: по 8 на каждый дом
        apartments = []
        for b in buildings:
            for k in range(1, 9):
                apt, _ = Apartment.objects.get_or_create(building=b, number=str(k))
                apartments.append(apt)

        interests = [[], ["INTERNET"], ["TV"], ["CCTV"], ["NANNY"], ["INTERNET","TV"], ["TV","CCTV"], ["INTERNET","CCTV","NANNY"]]
        satisf = ["1","2","3","4","5","SAT","UNSAT"]
        now = timezone.now()
        for i, apt in enumerate(apartments):
            for z in range(random.randint(2,4)):
                dt = now - timezone.timedelta(days=random.randint(0,60))
                vis = Visit.objects.create(
                    apartment=apt, visitor=random.choice([eng1, eng2, sv]),
                    visited_at=dt, latitude=apt.building.latitude, longitude=apt.building.longitude,
                    note=random.choice(["—", "Заинтересовался", "Слишком дорого", "Перезвонить через 2 месяца", "—", "Коммент инженера: новый жилец", "Договорились на оборудование"]))
                Survey.objects.create(
                    visit=vis,
                    client_profile=random.choice([
                        "Мужчина 40 лет, бизнесмен",
                        "Пожилая пара",
                        "Семья с детьми",
                        "Молодой студент",
                        "—",
                        "Работает дома",
                        "Безработный"
                    ]),
                    services_current=random.choice(interests),
                    provider_satisfaction=random.choice(satisf),
                    interested_services=random.choice(interests),
                    best_call_time=random.choice(["Утро","День","Вечер","После 18:00","Любое" ]),
                    contact_phone='+7 928 ' + str(random.randint(1000000,9999999)),
                    fair_price=random.choice([300, 500, 700, 1000, 1200, None]),
                    comment=random.choice(["", "Просил перезвонить в июле", "Очень недоволен скоростью", "Оставил заявку на видеонаблюдение", "Интересуют скидки"]),
                )
        self.stdout.write(self.style.SUCCESS("Seeded rich demo with roles assigned."))
