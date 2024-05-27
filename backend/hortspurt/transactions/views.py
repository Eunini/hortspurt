import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from userprofile.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests, json
from .utils import generateTransactionReference
from .models import AddMoneyTransaction
from .forms import AddMoneyTrForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from .tasks import confirm_transaction
load_dotenv()
# Create your views here.

bearer_token = 'Bearer ' + os.getenv('FLW_SECRET_KEY')
headers = {
    "Content-Type": "application/json",
    "Authorization": bearer_token
}


class PayWithPaystackView(View):
    def get(self, request):
        return render(request, 'pay_with_paystack.html')

    def post(self, request):
        return render(request, 'pay_with_paystack.html')

class PayWithFlwView(View):
    def get(self, request):
        return render(request, 'pay_with_flw.html')

    def post(self, request):
        return render(request, 'pay_with_flw.html')

class PayWithMonView(View):
    def get(self, request):
        return render(request, 'pay_with_mon.html')

    def post(self, request):
        return render(request, 'pay_with_mon.html')

class PayWithUssdView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pay_with_ussd.html')

    def post(self, request):
        account_bank = request.POST.get("account_bank")
        email = request.user.email
        full_name = request.user.get_full_name()
        amount = request.POST.get("amount")
        tx_ref = generateTransactionReference('100580192')
        data = {"account_bank": account_bank, "amount":int(amount), "currency":'NGN', "email":email, "fullname": full_name, "tx_ref": tx_ref}
 
        #print(data)
        res = requests.post('https://api.flutterwave.com/v3/charges?type=ussd', json=data, headers=headers)
        res_data = res.json()
        print(res_data)
        if (not res_data.get('status') or res_data['status'] != 'success'):
            msg = 'something went wrong, please try again'
        else:
            new_add_money_tr_form = AddMoneyTrForm({'user':request.user, 'amount':res_data['data'].get("amount"), 'tr_id':res_data['data'].get("id"), 'method':'U', 'status':'P'})
            if new_add_money_tr_form.is_valid():
                new_add_money_tr_form.save()
                ussdCode = res_data['meta']['authorization']['note']
                paymentCode = res_data['data']['payment_code']
                msg = f"To complete the payment, dial {ussdCode} from the mobile number linked to your bank account. If you're prompted for a payment code, enter {paymentCode}."
            else:
                print("form errors: ", new_add_money_tr_form.errors)
                msg = 'something went wrong, please try again'
        ctx = {'msg': msg}
        return render(request, 'dial_ussd_code.html', ctx)

@method_decorator(csrf_exempt, name='dispatch')
class FlwWebhook(View):
    def get(self, request):
        return render(request, 'pay_with_ussd.html')

    def post(self, request):
        secret_hash = os.getenv("FLW_SECRET_HASH")
        signature = request.headers.get('verif-hash')
        if (not signature or (signature != secret_hash)):
            return HttpResponse(status=401)
        payload = request.POST
        print("payload: ", payload)
        #event = payload.get('event')
        if payload:
            status = payload.get('status')
            tr_id = payload.get('id')

            if (not status or not tr_id):
                return HttpResponse(status=400)
            confirm_transaction.delay(tr_id)
            return HttpResponse(status=200)
        return HttpResponse(status=400)
