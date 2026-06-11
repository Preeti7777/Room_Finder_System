from django.urls import path
from . import views

urlpatterns = [
    path(
        'tenant_dashboard/',
        views.tenant_dashboard,
        name='tenant_dashboard'
    ),

    path(
        'landlord_dashboard/',
        views.landlord_dashboard,
        name='landlord_dashboard'
    ),

    path(
        'admin_dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),
]
