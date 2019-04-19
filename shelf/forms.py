from django import forms

from .models import Product, Stock, GroupSale


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
