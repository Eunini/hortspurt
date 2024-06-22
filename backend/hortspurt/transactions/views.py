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
import requests, json, traceback
from .utils import generateTransactionReference
from .models import AddMoneyTransaction
from .forms import AddMoneyTrForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from .tasks import confirm_transaction, test, confirm_transfer
load_dotenv()
# Create your views here.

bearer_token = 'Bearer ' + os.getenv('FLW_SECRET_KEY')
headers = {
    "Content-Type": "application/json",
    "Authorization": bearer_token
}

class PaymentOptionsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'payment_options.html')
    
    def post(self, request):
        return render(request, 'we_know.html')

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
        try:
            ctx = {}
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
                msg = 'USSD payment service is currently unavailable. Please try again'
            else:
                ctx['tr_id'] = res_data['data'].get("id")
                new_add_money_tr_form = AddMoneyTrForm({'user':request.user, 'amount':res_data['data'].get("amount"), 'tr_id':str(res_data['data'].get("id")), 'tr_ref':str(res_data['data'].get("tx_ref")), 'method':'U', 'status':'P'})
                if new_add_money_tr_form.is_valid():
                    new_add_money_tr_form.save()
                    ussdCode = res_data['meta']['authorization']['note']
                    paymentCode = res_data['data']['payment_code']
                    msg = f"To complete the payment, dial {ussdCode} from the mobile number linked to your bank account. If you're prompted for a payment code, enter {paymentCode}."
                else:
                    print("form errors: ", new_add_money_tr_form.errors)
                    msg = 'something went wrong, please try again'
            ctx['msg'] = msg
            return render(request, 'dial_ussd_code.html', ctx)
        except Exception as e:
            print(f"An error occurres: {e}")
            traceback.print_exc()
        return HttpResponse('Something went wrong, please try again')

class UssdVerifyView(LoginRequiredMixin, View):
    def get(self, request, tr_id):
        status = confirm_transaction(tr_id)
        print(status)
        if (status):
            return render(request, 'success.html')
        else:
            return render(request, 'paymenterror.html')


class PayWithTransferView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pay_with_bank.html')

    def post(self, request):
        try:
            ctx = {}
            email = request.user.email
            full_name = request.user.get_full_name()
            amount = request.POST.get("amount")
            tx_ref = generateTransactionReference('100580192')
            data = {"amount":int(amount), "currency":'NGN', "email":email, "tx_ref": tx_ref}
    
            print('tx_ref: ',tx_ref)
            res = requests.post('https://api.flutterwave.com/v3/charges?type=bank_transfer', json=data, headers=headers)
            res_data = res.json()
            print(res_data)
            if (not res_data.get('status') or res_data['status'] != 'success'):
                msg = 'Bank Transfer payment service is currently unavailable. Please try again'
            else:
                ctx['tr_ref'] = tx_ref
                transferAmount = res_data['meta']['authorization']['transfer_amount']
                new_add_money_tr_form = AddMoneyTrForm({'user':request.user, 'amount':transferAmount, 'tr_ref':tx_ref, 'method':'T', 'status':'P'})
                if new_add_money_tr_form.is_valid():
                    new_add_money_tr_form.save()
                    transferBank = res_data['meta']['authorization']['transfer_bank']
                    bankAccount = res_data['meta']['authorization']['transfer_account']
                    msg = f"To complete the payment,  transfer {transferAmount} to this bank account {bankAccount} {transferBank}"
                else:
                    print("form errors: ", new_add_money_tr_form.errors)
                    msg = 'something went wrong, please try again'
            ctx['msg'] = msg
            return render(request, 'bank_transfer.html', ctx)
        except Exception as e:
            print(f"An error occurres: {e}")
            traceback.print_exc()
        return HttpResponse('Something went wrong, please try again')

class TransferVerifyView(LoginRequiredMixin, View):
    def get(self, request, tr_id):
        status = confirm_transfer(tr_id)
        print(status)
        if (status):
            return render(request, 'success.html')
        else:
            return render(request, 'paymenterror.html')

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


class FlwWebhookTest(View):
    def get(self, request):
        print("Testing task...")
        #ct_task  = confirm_transaction.delay('1414862545')
        test.delay()
        # res = ct_task.get()
        # print(res)
        # print("Testing task...2")
        return HttpResponse('Done')