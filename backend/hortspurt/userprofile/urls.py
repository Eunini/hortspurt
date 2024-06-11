from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

app_name = 'home'
urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('data/', csrf_exempt(views.DataView.as_view()), name='data'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('coming-soon/', views.ComingSoonView.as_view(), name='comingsoon'),
    path('shoutout/', views.ShoutOutView.as_view(), name='shoutout'),
    path('my-profile/', views.ProfileView.as_view(), name='profile'),
]