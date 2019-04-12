from django import forms

from accounts.models import Pharmacy


class PharmacyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = (
            'name'
        )