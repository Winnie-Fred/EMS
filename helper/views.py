import requests
import os

from django.shortcuts import render

from dotenv import load_dotenv
load_dotenv()


# Create your views here.
def fetch_banks():
    url = 'https://api.paystack.co/bank'
    headers = {'Authorization': f'Bearer {os.getenv("PAYSTACK_SECRET_KEY", "paystack_secret_key")}'}
    bank_choices = []
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        bank_choices = [("---", "Select Bank")]
    else:
        if 'data' in response.json():
            banks = response.json()['data']
            bank_choices = [(f"{bank['name']}---{bank['code']}", bank['name']) for bank in banks]
        bank_choices = [("---", "Select Bank")] + bank_choices
    return bank_choices