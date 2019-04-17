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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'au-input au-input--full',
            }),
        }


class BranchRegistrationForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
        }


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
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
            'username': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'au-input au-input--full',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'au-input au-input--full',
            })
        }


class StaffSignInForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password',
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'au-input au-input--full',
                'autocomplete': 'off',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'au-input au-input--full',
            }),
        }
