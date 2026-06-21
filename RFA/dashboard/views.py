from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.models import User
from properties.models import Property
from accounts.forms import ProfileUpdateForm

@staff_member_required
def admin_dashboard(request):
    all_properties = Property.objects.all()
    landlords = User.objects.filter(role="LANDLORD")
    tenants = User.objects.filter(role="TENANT")

    pending_properties = (
        all_properties
        .filter(status="pending")
        .select_related("owner")
        .prefetch_related("images")
        .order_by("-created_at")[:6]
    )

    pending_certificates = (
        landlords
        .filter(verification_status="PENDING")
        .order_by("-date_joined")[:6]
    )

    context = {
        "total_users": User.objects.count(),
        "total_landlords": landlords.count(),
        "total_tenants": tenants.count(),

        "total_properties": all_properties.count(),
        "property_pending_count": all_properties.filter(status="pending").count(),
        "property_approved_count": all_properties.filter(status="approved").count(),
        "property_rejected_count": all_properties.filter(status="rejected").count(),

        "certificate_pending_count": landlords.filter(
            verification_status="PENDING"
        ).count(),

        "pending_properties": pending_properties,
        "pending_certificates": pending_certificates,
    }

    return render(request, "dashboard/admin_dashboard.html", context)


