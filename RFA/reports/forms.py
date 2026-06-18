from django import forms

from .models import PropertyReport
class PropertyReportForm(forms.ModelForm):
    class Meta:
        model = PropertyReport
        fields = ['reason', 'message']

        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain the issue briefly...'
            }),
        }