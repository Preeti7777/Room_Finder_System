from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth import authenticate


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'role',
            'profile_image',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid email or password.")

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if user is None:
            raise forms.ValidationError("Invalid email or password.")

        self.user = user

        return cleaned_data

    def get_user(self):
        return self.user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_image",
            "citizenship_front_image",
            "citizenship_back_image",
            "photo_with_citizenship"
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email address"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone number"
            }),
        }

class VerificationUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "citizenship_front_image",
            "citizenship_back_image",
            "photo_with_citizenship",
        ]

        widgets = {
            "citizenship_front_image": forms.FileInput(attrs={
                "class": "verify-file-input",
            }),
            "citizenship_back_image": forms.FileInput(attrs={
                "class": "verify-file-input",
            }),
            "photo_with_citizenship": forms.FileInput(attrs={
                "class": "verify-file-input",
            }),
        }