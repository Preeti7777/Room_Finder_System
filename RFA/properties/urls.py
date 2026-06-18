# properties/urls.py

from django.urls import path
from . import views
from reports import views as report_views
urlpatterns = [

    path(
        '',
        views.property_list,
        name='property_list'
    ),

    path(
        'add/',
        views.add_property,
        name='add_property'
    ),
    path(
        "districts/",
        views.get_districts_by_province,
        name="get_districts_by_province"
    ),
    path(
        'detail/<int:pk>/',
        views.property_detail,
        name='property_detail'
    ),
    path(
        'detail/<int:pk>/report/',
        report_views.report_property,
        name='report_property'
    ),
    path(
        "wishlist/",
        views.wishlist_list,
        name="wishlist_list"
    ),
    path(
        "wishlist/remove/<int:pk>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist"
    ),
    path(
        'wishlist/toggle/<int:pk>/',
        views.toggle_wishlist,
        name='toggle_wishlist'
    ),
    path(
    'detail/<int:pk>/reveal-phone/',
    views.reveal_phone_number,
    name='reveal_phone_number'
),
]
