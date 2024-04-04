from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profile
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
class BuyDataView(View):
    def get(self, request):
        return render(request, 'buy_data_input2.html')

    def post(self, request):
        return render(request, 'buy_data_input2.html')

class PayWithPaystackView(View):
    def get(self, request):
        return render(request, 'pay_with_paystack.html')

    def post(self, request):
        return render(request, 'pay_with_paystack.html')