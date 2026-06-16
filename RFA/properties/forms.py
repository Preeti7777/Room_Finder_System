from django.forms import ModelForm
from .location_data import NEPAL_PROVINCES_DISTRICTS
from django import forms
from .models import Facility, Property


class PropertyForm(forms.ModelForm):
    province = forms.ChoiceField(
        choices=[("", "Select province")] + [
            (province, province) for province in NEPAL_PROVINCES_DISTRICTS.keys()
        ],
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "provinceSelect"
        })
    )

    district = forms.ChoiceField(
        choices=[("", "Select district")],
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "districtSelect"
        })
    )

    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "property_type",
            "province",
            "district",
            "city",
            "area",
            "ward_number",
            "latitude",
            "longitude",
            "monthly_rent",
            "security_deposit",
            "available_date",
            "rules",
            "lalpurja_image",
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            selected_province = None

            if self.is_bound:
                selected_province = self.data.get("province")
            elif self.instance and self.instance.pk:
                selected_province = self.instance.province

            if selected_province in NEPAL_PROVINCES_DISTRICTS:
                self.fields["district"].choices = [("", "Select district")] + [
                    (district, district)
                    for district in NEPAL_PROVINCES_DISTRICTS[selected_province]
                ]
            else:
                self.fields["district"].choices = [("", "Select district")]


class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        exclude = ['property']
