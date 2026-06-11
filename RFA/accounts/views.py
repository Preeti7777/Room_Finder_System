from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import User
from .forms import UserRegistrationForm, LoginForm


def register_view(request):

    if request.method == 'POST':

        form = UserRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def login_view(request):

    # if request.user.is_authenticated:
    #     if request.user.is_staff:
    #         return redirect('admin_dashboard')
    #     elif request.user.role == User.Role.LANDLORD:
    #         return redirect('landlord_dashboard')
    #     elif request.user.role == User.Role.TENANT:
    #         return redirect('tenant_dashboard')
    #     else:
    #         return redirect('tenant_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')
            elif user.role == User.Role.LANDLORD:
                return redirect('landlord_dashboard')
            elif user.role == User.Role.TENANT:
                return redirect('tenant_dashboard')
            else:
                return redirect('tenant_dashboard')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })

def logout_view(request):
    logout(request)
    return redirect('login')