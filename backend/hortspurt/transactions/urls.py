from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'transactions'
urlpatterns = [
    path('data/', views.BuyDataView.as_view(), name='buy_data'),
    path('paywithpaystack/', views.PayWithPaystackView.as_view(), name='pay_with_paystack'),
    path('paywithflw/', views.PayWithFlwView.as_view(), name='pay_with_flw'),
    path('paywithussd/', views.PayWithUssdView.as_view(), name='pay_with_ussd'),
    path('flw-webhook/', views.FlwWebhook.as_view(), name='flw_webhook'),
]