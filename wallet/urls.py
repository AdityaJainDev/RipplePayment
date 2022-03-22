from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('code/', views.index, name='home'),
    path('payment/', views.payment, name='payment'),
    path('', views.generate_wallet, name='generate_wallet'),
    path('generate_wallet_car/', views.generate_wallet_car, name='generate_wallet_car'),
    path('success/', views.success, name='success'),
    path('transactions/', views.transactions, name='transactions'),
]
