from datetime import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from properties.models import Property
from accounts.models import User
from django.utils import timezone

@staff_member_required
def verification_list(request):
    status_filter = request.GET.get("status", "all")

    properties = Property.objects.select_related(
        "owner").order_by("-created_at")

    if status_filter in ("pending", "approved", "rejected"):
        properties = properties.filter(status=status_filter)

    paginator = Paginator(properties, 20)
    page = paginator.get_page(request.GET.get("page"))

    all_properties = Property.objects.all()
    stats = {
        "total":    all_properties.count(),
        "pending":  all_properties.filter(status="pending").count(),
        "approved": all_properties.filter(status="approved").count(),
        "rejected": all_properties.filter(status="rejected").count(),
    }

    return render(request, "verification/property_verification.html", {
        "page_obj":      page,
        "status_filter": status_filter,
        "stats":         stats,
    })


@staff_member_required
def verification_detail(request, pk):
    property = get_object_or_404(
        Property.objects.select_related("owner"),
        pk=pk,
    )
    return render(request, "verification/verification_detail.html", {
        "property": property,
    })


@staff_member_required
@require_POST
def approve_property(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if property.status == "approved":
        messages.info(request, f'"{property.title}" is already approved.')
        return redirect("verification_detail", pk=pk)

    property.status = "approved"
    property.reviewed_by = request.user
    property.reviewed_at = timezone.now()
    property.rejection_reason = ""          # clear any previous reason
    property.save(update_fields=["status", "reviewed_by", "reviewed_at", "rejection_reason"])

    messages.success(request, f'"{property.title}" has been approved.')
    return redirect("verification_list")


@staff_member_required
@require_POST
def reject_property(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if property.status == "rejected":
        messages.info(request, f'"{property.title}" is already rejected.')
        return redirect("verification_detail", pk=pk)

    reason = request.POST.get("rejection_reason", "").strip()

    if not reason:
        messages.error(request, "Please provide a rejection reason.")
        return redirect("verification_detail", pk=pk)

    property.status = "rejected"
    property.reviewed_by = request.user
    property.reviewed_at = timezone.now()
    property.rejection_reason = reason
    property.save(update_fields=["status", "reviewed_by", "reviewed_at", "rejection_reason"])

    messages.success(request, f'"{property.title}" has been rejected.')
    return redirect("verification_list")

@staff_member_required
def certificate_verification_list(request):
    status_filter = request.GET.get("status", "PENDING")

    landlords = User.objects.filter(
        role="LANDLORD"
    ).order_by("-date_joined")

    if status_filter in ("NOT_SUBMITTED", "PENDING", "VERIFIED", "REJECTED"):
        landlords = landlords.filter(verification_status=status_filter)

    paginator = Paginator(landlords, 20)
    page = paginator.get_page(request.GET.get("page"))

    all_landlords = User.objects.filter(role="LANDLORD")

    stats = {
        "total": all_landlords.count(),
        "not_submitted": all_landlords.filter(verification_status="NOT_SUBMITTED").count(),
        "pending": all_landlords.filter(verification_status="PENDING").count(),
        "verified": all_landlords.filter(verification_status="VERIFIED").count(),
        "rejected": all_landlords.filter(verification_status="REJECTED").count(),
    }

    return render(request, "verification/certificate_verification.html", {
        "page_obj": page,
        "status_filter": status_filter,
        "stats": stats,
    })

@staff_member_required
def certificate_verification_detail(request, user_id):
    landlord = get_object_or_404(
        User,
        pk=user_id,
        role="LANDLORD"
    )

    return render(request, "verification/certificate_verification_detail.html", {
        "landlord": landlord,
    })

@staff_member_required
@require_POST
def approve_certificate(request, user_id):
    landlord = get_object_or_404(
        User,
        pk=user_id,
        role="LANDLORD"
    )

    if landlord.verification_status == "VERIFIED":
        messages.info(request, f"{landlord.username} is already verified.")
        return redirect("certificate_verification_detail", user_id=user_id)

    if not landlord.has_submitted_verification_docs():
        messages.error(
            request,
            "Cannot approve. Required certificate documents are missing."
        )
        return redirect("certificate_verification_detail", user_id=user_id)

    landlord.verification_status = "VERIFIED"
    landlord.verification_rejection_reason = ""
    landlord.verified_at = timezone.now()

    landlord.save(update_fields=[
        "verification_status",
        "verification_rejection_reason",
        "verified_at",
    ])

    messages.success(
        request,
        f"{landlord.username}'s certificate has been approved."
    )

    return redirect("certificate_verification_list")

@staff_member_required
@require_POST
def reject_certificate(request, user_id):
    landlord = get_object_or_404(
        User,
        pk=user_id,
        role="LANDLORD"
    )

    reason = request.POST.get("rejection_reason", "").strip()

    if not reason:
        messages.error(request, "Please provide a rejection reason.")
        return redirect("certificate_verification_detail", user_id=user_id)

    landlord.verification_status = "REJECTED"
    landlord.verification_rejection_reason = reason
    landlord.verified_at = None

    landlord.save(update_fields=[
        "verification_status",
        "verification_rejection_reason",
        "verified_at",
    ])

    messages.success(
        request,
        f"{landlord.username}'s certificate has been rejected."
    )

    return redirect("certificate_verification_list")