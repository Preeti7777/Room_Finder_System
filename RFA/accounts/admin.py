from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "phone",
        "verification_status",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "verification_status",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "verified_at",
        "citizenship_front_preview",
        "citizenship_back_preview",
        "photo_with_citizenship_preview",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "User Role & Profile",
            {
                "fields": (
                    "role",
                    "phone",
                    "profile_image",
                )
            },
        ),
        (
            "Landlord Verification",
            {
                "fields": (
                    "verification_status",
                    "verification_rejection_reason",
                    "verified_at",

                    "citizenship_front_image",
                    "citizenship_front_preview",

                    "citizenship_back_image",
                    "citizenship_back_preview",

                    "photo_with_citizenship",
                    "photo_with_citizenship_preview",
                )
            },
        ),
    )

    def citizenship_front_preview(self, obj):
        if obj.citizenship_front_image:
            return format_html(
                '<a href="{}" target="_blank">View citizenship front</a>',
                obj.citizenship_front_image.url
            )
        return "No front image uploaded"

    def citizenship_back_preview(self, obj):
        if obj.citizenship_back_image:
            return format_html(
                '<a href="{}" target="_blank">View citizenship back</a>',
                obj.citizenship_back_image.url
            )
        return "No back image uploaded"

    def photo_with_citizenship_preview(self, obj):
        if obj.photo_with_citizenship:
            return format_html(
                '<a href="{}" target="_blank">View photo with citizenship</a>',
                obj.photo_with_citizenship.url
            )
        return "No photo uploaded"

    citizenship_front_preview.short_description = "Citizenship Front Preview"
    citizenship_back_preview.short_description = "Citizenship Back Preview"
    photo_with_citizenship_preview.short_description = "Photo With Citizenship Preview"