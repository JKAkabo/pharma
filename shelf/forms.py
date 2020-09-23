from django import forms
from django.forms import formset_factory, BaseModelFormSet
from .models import Branch, Product, Stock, GroupSale, Sale, UserProfile
from django.core.files.images import get_image_dimensions


class AddBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            })
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'active_ingredients',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': '',
            }),
            'active_ingredients': forms.Textarea(attrs={
                'class': 'form-control',
            })
        }


class AddToStockForm(forms.Form):
    products = Product.objects.all()

    product = forms.ModelChoiceField(products, widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    units = forms.IntegerField(min_value=1, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': '',
    }))


class AddSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (
            'product',
            'units_sold',
        )
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'required': '',
            }),
            'units_sold': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': '',
            })
        }


AddSaleFormSet = formset_factory(AddSaleForm)
AddToStockFormSet = formset_factory(AddToStockForm)
AddProductFormSet = formset_factory(AddProductForm)



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'avatar',
        )

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            max_width = max_height= 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar         
