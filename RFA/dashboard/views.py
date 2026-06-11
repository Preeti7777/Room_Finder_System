from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def tenant_dashboard(request):
    return render(request, 'dashboard/tenant_dashboard.html', {
        'user': request.user
    })


@login_required
def landlord_dashboard(request):
    return render(request, 'dashboard/landlord_dashboard.html',{
        'user': request.user
    })


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html', {
        'user': request.user
    })
