from django.shortcuts import render

# Create your views here.
from properties.models import Property
from .models import PropertyReport
from .forms import PropertyReportForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

@login_required
def report_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.user == property_obj.owner:
        messages.error(request, "You cannot report your own property.")
        return redirect('property_detail', pk=property_obj.pk)

    existing_report = PropertyReport.objects.filter(
        property=property_obj,
        reported_by=request.user
    ).first()

    if existing_report:
        messages.warning(request, "You have already reported this property.")
        return redirect('property_detail', pk=property_obj.pk)

    if request.method == 'POST':
        form = PropertyReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.property = property_obj
            report.reported_by = request.user
            report.save()

            messages.success(request, "Your report has been submitted successfully.")
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyReportForm()

    return render(request, 'reports/report_property.html', {
        'form': form,
        'property': property_obj
    })

@login_required
def my_reports(request):
    reports = PropertyReport.objects.filter(
        reported_by=request.user
    ).select_related(
        'property',
        'property__owner'
    ).order_by('-created_at')

    return render(request, 'reports/my_reports.html', {
        'reports': reports
    })