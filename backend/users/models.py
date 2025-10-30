from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("engineer", "Engineer"),
        ("supervisor", "Supervisor"),
        ("admin", "Admin"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="engineer")

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
