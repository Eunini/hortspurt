import os
from dotenv import load_dotenv
from celery import shared_task 
import requests, json
from django.http import JsonResponse, HttpResponse
from .models import AddMoneyTransaction
load_dotenv()

bearer_token = 'Bearer ' + os.getenv('FLW_SECRET_KEY')
headers = {
    "Content-Type": "application/json",
    "Authorization": bearer_token
}

@shared_task
def confirm_transaction(tr_id):
    try:
        confirmation_url = f'https://api.flutterwave.com/v3/transactions/{tr_id}/verify'
        try:
            tr_obj = AddMoneyTransaction.objects.get(id=tr_id)
            print(f"Transaction with ID {tr_id} found: {tr_obj}")

            try:
                response = requests.post(confirmation_url, headers=headers)
                response.raise_for_status()

                try:
                    res_data = response.json()
                    if (res_data['status'] == 'success' and res_data['data']['currency'] == 'NGN' and res_data['data']['amount'] == tr_obj.amount):
                        print("Accurate!")
                        if (tr_obj.status != 'S'):
                            tr_obj.status = 'S'
                            tr_obj.save()
                            print(tr_obj.user.profile.wallet_balance, tr_obj.amount)
                            tr_obj.user.profile.wallet_balance += tr_obj.amount
                            print(tr_obj.user.profile.wallet_balance)
                            tr_obj.user.profile.save()
                            return
                    print(f"Transaction not confirmed: {res_data['error']}")
                    tr_obj.status = 'F'
                    tr_obj.save()
                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Error parsing request: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Error making request: {e}")

        except AddMoneyTransaction.DoesNotExist:
            print(f"Transaction with ID {tr_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
