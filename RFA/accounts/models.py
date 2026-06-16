from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField


class User(AbstractUser):

    class Role(models.TextChoices):
        TENANT = "TENANT", "Tenant"
        LANDLORD = "LANDLORD", "Landlord"

    class VerificationStatus(models.TextChoices):
        NOT_SUBMITTED = "NOT_SUBMITTED", "Not Submitted"
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.TENANT
    )

    phone = models.CharField(max_length=15, blank=True, null=True)

    profile_image = CloudinaryField(
        'profile_image',
        blank=True,
        null=True
    )

    citizenship_front_image = CloudinaryField(
        'citizenship_front',
        blank=True,
        null=True
    )

    citizenship_back_image = CloudinaryField(
        'citizenship_back',
        blank=True,
        null=True
    )

    photo_with_citizenship = CloudinaryField(
        'photo_with_citizenship',
        blank=True,
        null=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_SUBMITTED
    )

    verification_rejection_reason = models.TextField(
        blank=True,
        null=True
    )

    verified_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def has_submitted_verification_docs(self):
        return (
            self.citizenship_front_image and
            self.citizenship_back_image and
            self.photo_with_citizenship
        )

    def can_add_property(self):
        return (
            self.role == self.Role.LANDLORD and
            self.verification_status == self.VerificationStatus.VERIFIED
        )

    def __str__(self):
        return f"{self.username} ({self.role})"