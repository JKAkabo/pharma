from django.contrib import admin

# Register your models here.

from .models import GroupSale, Product, Sale, Stock, Upload

admin.site.register(GroupSale)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Stock)
admin.site.register(Upload)
