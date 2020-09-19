from django import forms
from django.forms import formset_factory, BaseModelFormSet
from .models import Branch, Product, Stock, GroupSale, Sale


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

# image upload form
from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):

    class Meta:
        model = Upload
        fields = ['image']
        