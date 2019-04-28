from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_pharmacy, name='register_pharmacy'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]