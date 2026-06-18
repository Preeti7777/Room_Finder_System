from django.db import models
from django.conf import settings
from properties.models import Property
# Create your models here.
class PropertyReport(models.Model):
    REASON_CHOICES = [
        ('fake_listing', 'Fake Listing'),
        ('wrong_information', 'Wrong Information'),
        ('already_rented', 'Already Rented'),
        ('suspicious_landlord', 'Suspicious Landlord'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='property_reports'
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    message = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'reported_by')

    def __str__(self):
        return f"{self.reported_by} reported {self.property.title}"