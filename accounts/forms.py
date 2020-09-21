from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Branch, Pharmacy, Staff
from django.core.files.images import get_image_dimensions



class PharmacyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = (
            'name',
            'email',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pharmacy Name',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pharmacy Email',
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
                'class': 'form-control',
                'placeholder': 'Branch Name',
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
                'class': 'form-control',
                'placeholder': 'First Name',
                'autocomplete': 'off',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'autocomplete': 'off',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            })
        }


class StaffLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

class StaffPictureForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = (
            'profile_picture',
        )
 
