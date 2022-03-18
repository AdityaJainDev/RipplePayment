from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.index, name='home'),
    path('payment/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
]
