from django import forms
from django.forms import formset_factory, BaseModelFormSet
from .models import Product, Stock, GroupSale, Sale


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'active_ingredients',
        )


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
