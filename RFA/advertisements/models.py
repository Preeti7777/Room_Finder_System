from django.db import models


class Advertisement(models.Model):
    AD_TYPE_CHOICES = [
        ('banner', 'Banner Ad'),
        ('rewarded', 'Rewarded Ad'),
    ]

    POSITION_CHOICES = [
        ('homepage_top', 'Homepage Top Banner'),
        ('homepage_between_cards', 'Homepage Between Cards'),
        ('detail_below_images', 'Listing Detail Below Images'),
        ('phone_reveal', 'Phone Reveal Rewarded Ad'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='advertisements/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    link = models.URLField(blank=True, null=True)

    ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPE_CHOICES,
        default='banner'
    )

    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES
    )

    duration_seconds = models.PositiveIntegerField(default=5)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_position_display()}"