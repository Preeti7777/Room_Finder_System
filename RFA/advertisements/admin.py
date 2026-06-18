from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'ad_type',
        'position',
        'duration_seconds',
        'is_active',
        'created_at',
    )

    list_filter = (
        'ad_type',
        'position',
        'is_active',
    )

    search_fields = (
        'title',
        'description',
    )

    list_editable = (
        'is_active',
    )