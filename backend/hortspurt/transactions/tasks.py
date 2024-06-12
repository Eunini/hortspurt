import os
from dotenv import load_dotenv
from celery import shared_task 
import requests, json
from django.http import JsonResponse, HttpResponse
from .models import AddMoneyTransaction
import logging, traceback
load_dotenv()

bearer_token = 'Bearer ' + os.getenv('FLW_SECRET_KEY')
headers = {
    "Content-Type": "application/json",
    "Authorization": bearer_token
}

@shared_task(bind=True)
def test(self):
    for i in range(10):
        print(i)
    return 'Done'

@shared_task
def confirm_transaction(tr_id):
    try:
        confirmation_url = f'https://api.flutterwave.com/v3/transactions/{tr_id}/verify'
        try:
            tr_obj = AddMoneyTransaction.objects.get(tr_id=tr_id)
            if (tr_obj.status == 'S'):
                return True

            print(f"Transaction with ID {tr_id} found: {tr_obj}")

            try:
                response = requests.get(confirmation_url, headers=headers)
                response.raise_for_status()

                try:
                    res_data = response.json()
                    if (res_data['status'] == 'success'):
                        if (res_data['data']['status'] == 'successful' and res_data['data']['currency'] == 'NGN' and res_data['data']['amount'] == tr_obj.amount):
                            print("Accurate!")
                            print(res_data)
                            if (tr_obj.status != 'S'):
                                tr_obj.status = 'S'
                                tr_obj.save()
                                print(tr_obj.user.profile.wallet_balance, tr_obj.amount)
                                tr_obj.user.profile.wallet_balance += tr_obj.amount
                                print(tr_obj.user.profile.wallet_balance)
                                tr_obj.user.profile.save()
                                return True
                            elif (res_data['data']['status'] == 'failed'):
                                tr_obj.status = 'F'
                                tr_obj.save()
                                print(f"Transaction not confirmed: {res_data['data']['processor_response']}")
                    else:
                        print(f"Transaction not verified: {res_data['status']}")
                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Error parsing request: {e}")
                    traceback.print_exc()
            except requests.exceptions.RequestException as e:
                print(f"Error making request: {e}")

        except AddMoneyTransaction.DoesNotExist:
            print(f"Transaction with ID {tr_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

test.delay()
#requests.get("http://127.0.0.1:8000/purchase/test/")