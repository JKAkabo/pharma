from django import forms

from .models import Product, Stock, GroupSale


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'active_ingredients',
        )


class AddStockForm(forms.Form):
    units = forms.IntegerField(min_value=1)
