from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from properties.models import Property


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
    # property.reviewed_by = request.user
    property.save(update_fields=["status"])

    messages.success(request, f'"{property.title}" has been approved.')
    return redirect("verification_list")


@staff_member_required
@require_POST
def reject_property(request, pk):
    property = get_object_or_404(Property, pk=pk)

    if property.status == "rejected":
        messages.info(request, f'"{property.title}" is already rejected.')
        return redirect("verification_detail", pk=pk)

    property.status = "rejected"
    # property.reviewed_by = request.user
    # property.rejection_reason = request.POST.get("rejection_reason", "").strip()
    property.save(update_fields=["status"])

    messages.success(request, f'"{property.title}" has been rejected.')
    return redirect("verification_list")


# @staff_member_required
# @require_POST
# def bulk_action(request):
#     action = request.POST.get("action")
#     ids = request.POST.getlist("property_ids")
#     valid_actions = ("approve", "reject")

#     if action not in valid_actions or not ids:
#         messages.error(
#             request, "Invalid bulk action or no properties selected.")
#         return redirect("verification_list")

#     new_status = "approved" if action == "approve" else "rejected"
#     updated = Property.objects.filter(pk__in=ids).update(
#         status=new_status,
#         reviewed_by=request.user,
#     )

#     messages.success(
#         request, f"{updated} propert{'y' if updated == 1 else 'ies'} {new_status}.")
#     return redirect("verification_list")


# ── Landlord-facing views ─────────────────────────────────────────────────────

# @login_required
# def my_properties(request):
#     properties = Property.objects.filter(owner=request.user).order_by("-created_at")
#     return render(request, "admin_panel/my_properties.html", {
#         "properties": properties,
#     })


# @login_required
# def my_property_detail(request, pk):
#     property = get_object_or_404(Property, pk=pk, owner=request.user)
#     return render(request, "admin_panel/my_property_detail.html", {
#         "property": property,
#     })
