import random
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from properties.models import Property, Wishlist
from .models import User,EmailOTP
from django.core.mail import send_mail
from .forms import ProfileUpdateForm, UserRegistrationForm, LoginForm, VerificationUploadForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            user = form.save(commit=False)

            # Activate the user immediately
            user.email_verified = True
            user.is_active = True
            user.save()

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect('login')  # Change this if your login URL name is different

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                return redirect('profile')
            else:
                return redirect('property_list')

        elif getattr(form, "inactive_user", None):
            request.session['verify_user_id'] = form.inactive_user.id

            messages.error(
                request,
                "Please verify your email before logging in."
            )

            return redirect('verify_email_otp')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('property_list')


@login_required
def profile_view(request):
    profile_user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")

        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileUpdateForm(instance=profile_user)

    my_properties = (
        Property.objects
        .filter(owner=profile_user)
        .prefetch_related("images", "facility")
        .order_by("-created_at")
    )

    wishlist_items = (
        Wishlist.objects
        .filter(user=profile_user)
        .select_related("property")
        .prefetch_related("property__images")
        .order_by("-created_at")
    )

    all_properties = Property.objects.all()
    landlord_users = User.objects.filter(role="LANDLORD")
    tenant_users = User.objects.filter(role="TENANT")

    pending_certificates = landlord_users.filter(
        verification_status="PENDING"
    )

    context = {
        "profile_user": profile_user,
        "form": form,

        # Landlord data
        "my_properties": my_properties[:5],
        "total_listings": my_properties.count(),
        "approved_count": my_properties.filter(status="approved").count(),
        "pending_count": my_properties.filter(status="pending").count(),
        "rejected_count": my_properties.filter(status="rejected").count(),

        # Tenant data
        "wishlist_items": wishlist_items[:5],
        "wishlist_count": wishlist_items.count(),

        # Admin/staff data
        "total_users": User.objects.count(),
        "total_landlords": landlord_users.count(),
        "total_tenants": tenant_users.count(),
        "total_properties": all_properties.count(),
        "property_pending_count": all_properties.filter(status="pending").count(),
        "property_approved_count": all_properties.filter(status="approved").count(),
        "property_rejected_count": all_properties.filter(status="rejected").count(),
        "certificate_pending_count": pending_certificates.count(),
        "recent_pending_properties": all_properties.filter(status="pending").select_related("owner").order_by("-created_at")[:5],
        "recent_pending_certificates": pending_certificates.order_by("-date_joined")[:5],
    }

    return render(request, "accounts/profile.html", {**context, "form": form})

@login_required
def verify_account_view(request):
    if request.user.role != "LANDLORD":
        messages.error(request, "Only landlords can submit verification documents.")
        return redirect("profile")

    if request.method == "POST":
        form = VerificationUploadForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            user = form.save(commit=False)

            if (
                user.citizenship_front_image and
                user.citizenship_back_image and
                user.photo_with_citizenship
            ):
                if user.verification_status != "VERIFIED":
                    user.verification_status = "PENDING"
                    user.verification_rejection_reason = ""

                user.save()

                messages.success(
                    request,
                    "Verification documents submitted successfully. Please wait for admin approval."
                )
                return redirect("profile")

            messages.error(request, "Please upload all required verification documents.")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = VerificationUploadForm(instance=request.user)

    return render(request, "accounts/verify_account.html", {
        "form": form,
        "profile_user": request.user,
    })

def verify_email_otp(request):
    user_id = request.session.get('verify_user_id')

    if not user_id:
        messages.error(request, "Verification session expired. Please register again.")
        return redirect('register')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        try:
            otp_obj = EmailOTP.objects.get(user=user)
        except EmailOTP.DoesNotExist:
            messages.error(request, "OTP not found. Please register again.")
            return redirect('register')

        if otp_obj.is_expired():
            otp_obj.delete()
            messages.error(request, "OTP expired. Please register again.")
            return redirect('register')

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP.")
            return redirect('verify_email_otp')

        user.email_verified = True
        user.is_active = True
        user.save()

        otp_obj.delete()

        request.session.pop('verify_user_id', None)

        messages.success(request, "Email verified successfully. You can now login.")
        return redirect('login')

    return render(request, 'accounts/verify_email_otp.html')

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user

        # Log the user out first
        logout(request)

        # Delete the account
        user.delete()

        messages.success(
            request,
            "Your account has been deleted successfully."
        )

        return redirect("property_list")  # Change if your home page URL name is different

    return redirect("profile")