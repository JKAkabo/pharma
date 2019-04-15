from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Branch, Pharmacy


class PharmacyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = (
            'name',
            'email',
        )


class BranchRegistrationForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = (
            'name',
        )


class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )


class StaffSignInForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
        )