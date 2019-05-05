from django.urls import path

from . import views

app_name = 'shelf'

urlpatterns = [
    path('sale/add/', views.add_sale, name='add_group_sale'),
    path('sale/<uuid:group_sale_id>/receipt/', views.group_sale_receipt, name='group_sale_receipt'),
    path('branches/', views.list_branches, name='list_branches'),
]