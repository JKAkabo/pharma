from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Branch, Pharmacy, UserImage
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

class UserImageForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = (
            'user',
            'profile_pic',
        )

        def clean_avatar(self):
            profile_pic = self.cleaned_data['profile_pic']

            try:
                w, h = get_image_dimensions(profile_pic)

                #validate dimensions
                max_width = max_height = 100
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                        '%s x %s pixels or smaller.' % (max_width, max_height))

                #validate content type
                main, sub = profile_pic.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')

                #validate file size
                if len(profile_pic) > (20 * 1024):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 20k.')

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass

            return profile_pic    
 
