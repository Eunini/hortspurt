from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

app_name = 'buy'
urlpatterns = [
    path('data/', views.BuyDataView.as_view(), name='buy_data'),
]