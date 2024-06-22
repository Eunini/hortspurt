import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.views import View
from .params import MTN_SME, MOBILE9_GFT, AIRTEL_GFT, GLO_GFT
import requests
from django.http import JsonResponse, HttpResponse
from transactions.utils import generateTransactionReference
from django.core.exceptions import ValidationError
from .husmo import MTN_PLANS, MOBILE9_PLANS, GLO_PLANS, AIRTEL_PLANS
from .models import BuyAirtimeData
load_dotenv()
# Create your views here.

base_url = "https://www.husmodata.com/api"
NPS = {'MTN':1, 'GLO':2, 'AIRTEL':4, '9MOBILE':3}
CODES = [13, 14, 234, 255]
HUSMO_API_KEY = os.getenv('HUSMO_API_KEY')
headers = {"Content-Type": "application/json", "Authorization": "Token 7714689b20c84d918f3f96e7e16fcf291fb7bc4e"}

def refund(user, price):
    try:
        user.profile.wallet_balance += price
        user.profile.full_clean()  # This will trigger the validation
        user.profile.save()
        return price
    except ValidationError as e:
        print(f"ValidationError: {e}")
    return False

def verify(NP, phone_no, code):
    if NP not in NPS.keys():
        return False
    if code not in CODES:
        return False
    if len(phone_no) < 11:
        return False
    if phone_no[:4] == '+234':
        phone_no = '0' + phone_no[4:]
    if (len(phone_no) != 11):
        return False
    return True

def deduct_balance(user, NP, code):
    print(NP, code)
    if (NP == 'MTN'):
        plans = MTN_PLANS
    elif (NP == 'GLO'):
        plans = GLO_PLANS
    elif (NP == 'AIRTEL'):
        plans = AIRTEL_PLANS
    elif (NP == '9MOBILE'):
        plans = MOBILE9_PLANS
    else:
        return False

    for plan in plans:
        if plan['data_id'] == code:
            price = int(plan['amount'])
            print(price, user.profile.wallet_balance)
    if ( price <= user.profile.wallet_balance):
        try:
            user.profile.wallet_balance -= price
            user.profile.full_clean()  # This will trigger the validation
            user.profile.save()
            return price
        except ValidationError as e:
            print(f"ValidationError: {e}")
    return False

class BuyDataView(View):
    def get(self, request):
        phone_number = request.user.username
        phone_number = phone_number[1:]
        ctx = {'MTN_PLANS': MTN_PLANS, '9MOBILE_PLANS': MOBILE9_PLANS, 'GLO_PLANS': GLO_PLANS, 'AIRTEL_PLANS': AIRTEL_PLANS, 'phone_number':phone_number}
        return render(request, 'buy_data.html', ctx)

    def post(self, request):
        endpoint_url = base_url+"/data/"
        data = request.POST
        print(data)
        NP = data.get("NP")
        phone_no = data.get("phonenofield")
        try:
            code = int(data.get("code"))
        except ValueError as e:
            print(e)
            return HttpResponse(status=400)

        if (not NP or not phone_no or not code):
            return HttpResponse(status=400)
        data_is_valid = verify(NP, phone_no, code)
        if (not data_is_valid):
            print('Invalid data NP:', NP, ' phone_no:', phone_no, ' code:',code)
            return HttpResponse(status=400)
        service = NPS[NP]
        print(service, phone_no, code)
        data={"network": service, "mobile_number": phone_no, "plan": code, "Ported_number": False}
        price = deduct_balance(request.user, NP, code)
        if (price):
            try:    
                res = requests.post(endpoint_url, json=data, headers=headers)
                print(res)
                if (res.status_code == 201):
                    res_data = res.json()
                    print(res_data)
                    if (res_data['Status'] == 'successful'):

                        return render(request, 'success.html')
                print(res.status_code)
                refund(request.user, price)
                return HttpResponse(status=500)
            except (ConnectionError, KeyError, ValueError) as e:
                print(e)
                refund(request.user, price)
                return HttpResponse(status=500)
        else:
            msg = 'Purchase unsuccessful, insufficient balance'
            return HttpResponse(msg, status=402, content_type="text/html")

class PadiView(View):
    def get(self, request):
        ctx = {'MTN_PLANS': MTN_PLANS, '9MOBILE_PLANS': MOBILE9_PLANS, 'GLO_PLANS': GLO_PLANS, 'AIRTEL_PLANS': AIRTEL_PLANS}
        return render(request, 'padi.html', ctx)

    def post(self, request):
        endpoint_url = base_url+"/data/"
        data = request.POST
        print(data)
        NP = data.get("NP")
        phone_no = data.get("phonenofield")
        try:
            code = int(data.get("code"))
        except ValueError as e:
            print(e)
            return HttpResponse(status=400)
    
        if (not NP or not phone_no or not code):
            return HttpResponse(status=400)
        data_is_valid = verify(NP, phone_no, code)
        if (not data_is_valid):
            print('Invalid data NP:', NP, ' phone_no:', phone_no, ' code:',code)
            return HttpResponse(status=400)
        service = NPS[NP]
        print(service, phone_no, code)
        data={"network": service, "mobile_number": phone_no, "plan": code, "Ported_number": False}
        price = deduct_balance(request.user, NP, code)
        if (price):
            try:    
                res = requests.post(endpoint_url, json=data, headers=headers)
                print(res)
                if (res.status_code == 201):
                    res_data = res.json()
                    print(res_data)
                    if (res_data['Status'] == 'successful'):
                        return render(request, 'success.html')
                print(res.status_code)
                refund(request.user, price)
                return HttpResponse(status=500)
            except (ConnectionError, KeyError, ValueError) as e:
                print(e)
                refund(request.user, price)
                return HttpResponse(status=500)
        else:
            msg = 'Purchase unsuccessful, insufficient balance'
            return HttpResponse(msg, status=402, content_type="text/html")

# class BuyDataView(View):
#     def get(self, request):
#         ctx = {'MTN_PLANS': MTN_SME, '9MOBILE_PLANS': MOBILE9_GFT, 'AIRTEL_PLANS': AIRTEL_GFT, 'GLO_PLANS': GLO_GFT}
#         return render(request, 'buy_data.html', ctx)

#     def post(self, request):
#         endpoint_url = base_url+"/data"
#         data = request.POST
#         print(data)
#         NP = data.get("NP")
#         phone_no = data.get("phonenofield")
#         code = data.get("code")
#         if (not NP or not phone_no or not code):
#             return HttpResponse(status=400)
#         data_is_valid = verify(NP, phone_no, code)
#         if (not data_is_valid):
#             print('Invalid data NP:', NP, ' phone_no:', phone_no, ' code ',code)
#             return HttpResponse(status=400)
#         service = NPS[NP]
#         ref = generateTransactionReference(str(request.user.id))
#         data={'apikey': HUSMO_API_KEY, 'service': service, 'MobileNumber': phone_no, 'DataPlan': code, 'ref': ref}
#         if (deduct_balance(request.user, NP, code)):     
#             res = requests.post(endpoint_url, data=data, headers=headers)
#             res_data = res.json()
#             if (res_data['description']['status_description'] == 'TRANSACTION SUCCESSFUL'):
#                 return render(request, 'success.html')
#             else:
#                 refund(user, code)
#                 return HttpResponse(status=500)
#         else:
#             msg = 'Purchase unsuccessful, insufficient balance'
#             return HttpResponse(msg, status=402, content_type="text/html")