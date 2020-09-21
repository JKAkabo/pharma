from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pharma.settings import base


from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register_pharmacy, name='register_pharmacy'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)