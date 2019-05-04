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


class AddStockForm(forms.Form):
    units = forms.IntegerField(min_value=1)


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


AddSaleFormSet = formset_factory(AddSaleForm, can_delete=True)
