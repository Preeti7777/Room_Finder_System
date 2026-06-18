from django.contrib import admin

from .models import PropertyReport

# Register your models here.
@admin.register(PropertyReport)
class PropertyReportAdmin(admin.ModelAdmin):
    list_display = ('property', 'reported_by', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('property__title', 'reported_by__email', 'message')
    list_editable = ('status',)