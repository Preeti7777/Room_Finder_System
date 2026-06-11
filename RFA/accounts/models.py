from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class User(AbstractUser):

    class Role(models.TextChoices):
        TENANT = "TENANT", "Tenant"
        LANDLORD = "LANDLORD", "Landlord"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TENANT
    )

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_image = CloudinaryField(
        'image',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"