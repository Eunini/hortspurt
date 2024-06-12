from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'transactions'
urlpatterns = [
    path('paystack/', views.PayWithPaystackView.as_view(), name='pay_with_paystack'),
    path('flw/', views.PayWithFlwView.as_view(), name='pay_with_flw'),
    path('ussd/', views.PayWithUssdView.as_view(), name='pay_with_ussd'),
    path('ussd/verify/<int:tr_id>/', views.UssdVerifyView.as_view(), name='ussd_verify'),
    path('mon/', views.PayWithMonView.as_view(), name='pay_with_mon'),
    path('flwwebhook/', views.FlwWebhook.as_view(), name='flw_webhook'),
    path('test/', views.FlwWebhookTest.as_view(), name='flw_webhook_test'),
]