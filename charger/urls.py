from django.urls import path
from . import views

app_name = 'charger'

urlpatterns = [
    path('create_payment', views.create_payment, name='create_payment'),
    path('show_details', views.show_details, name='show_details'),
    path('transactions', views.transactions, name='transactions'),
    path('new_details', views.new_details, name='new_details'),
]