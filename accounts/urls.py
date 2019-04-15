from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_pharmacy, name='register_pharmacy'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),

]