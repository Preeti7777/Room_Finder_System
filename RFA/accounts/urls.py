from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),
    path(
        "verify-account/",
        views.verify_account_view,
        name="verify_account"
    ),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html",
            success_url=reverse_lazy("profile")
        ),
        name="change_password"
    ),
    path(
        'verify-email/',
        views.verify_email_otp,
        name='verify_email_otp'
    ),
    path("delete-account/", views.delete_account, name="delete_account"),
]
