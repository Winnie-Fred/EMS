import os
import requests
import json 

from typing import Type
from requests.exceptions import RequestException

from django.db.models import Model
from django.utils.crypto import get_random_string

from .models import Tenancy, PaymentStatus

SAAS_PERCENTAGE_CHARGE_PROPERTY = 0.1

SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
AUTH_HEADER = f"Bearer {SECRET_KEY}"
PAYSTACK_INITIALIZE_URL = os.getenv("PAYSTACK_INITIALIZE_PAYMENT_URL", "paystack_initialize_payment_url")
PAYSTACK_VERIFY_PAYMENT_URL_ROOT = os.getenv("PAYSTACK_VERIFY_PAYMENT_URL_ROOT", "paystack_verify_payment_url_root")

def generate_unique_reference(instance: Type[Model], new_ref=None, char_length=64) -> str:
    ''' 
    Generates a unique reference code of 64 [default] characters 
    for the reference field of an instance Model.

    Note: The model MUST have a field [reference]
    '''
    if new_ref:
        ref = new_ref
    else:
        ref = get_random_string(char_length)

    instance_class = instance.__class__
    qs = instance_class.objects.filter(reference=ref)

    if qs.exists():
        new_ref = get_random_string(char_length)
        return generate_unique_reference(instance, new_ref=new_ref)

    return ref

def initialize_payment(email, amount, reference, metadata="", callback_url="http://127.0.0.1:8000/payment_callback/"):
    '''
    function for initializing payments.

    params are (email, amount, reference, metadata and callback_url)

    returns an Authorization URL.
    '''

    url = PAYSTACK_INITIALIZE_URL

    amount *= 100 #  convert amount to kobo value

    try:
        response = requests.post(
            url,
            json={
                'email': email,
                'amount': str(amount),
                'reference': reference,
                'callback_url': callback_url,
                'metadata':metadata,
            },
            headers={
                'Authorization': AUTH_HEADER
            }
        )

        response_dict = response.json()
        if response_dict['status'] == True:
            return response_dict['data']['authorization_url']
        else:
            print(response_dict)
        
    except RequestException as e:
        print(e)
    return ''

def verify_payment(reference):
    url = f"{PAYSTACK_VERIFY_PAYMENT_URL_ROOT}/{reference}"

    try:
        response = requests.get(
            url,
            headers={
                'Authorization': AUTH_HEADER
            }
        )

        response_dict = response.json()
        if response_dict["data"]["status"] == "success":
            return response_dict
    except RequestException as e:
        print(e)

    return {}

def _get_recipient_code(recipient):
    recipient_data = {
        "type": "nuban", 
        "name": recipient.get_full_name(), 
        "account_number": recipient.userprofile.account_number, 
        "bank_code": recipient.userprofile.bank_code, 
        "currency": "NGN"
    }
    headers = {
        'Authorization': AUTH_HEADER,      
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://api.paystack.co/transferrecipient", data=json.dumps(recipient_data), headers=headers)
    except RequestException as e:
        print(e)
    else:
        if response:
            response_dict = response.json()
            if response_dict["status"] == "true":
                print(response_dict["data"]["recipient_code"])
                return response_dict["data"]["recipient_code"]
    return ''


def transfer_to_property_lister(amount, recipient, reference, reason):
    recipient_code = _get_recipient_code(recipient)
    transfer_data = {
        "source": "balance", 
        "amount": amount,
        "reference": reference, 
        "recipient": recipient_code, 
        "reason": reason 
    }
    headers = {
        'Authorization': AUTH_HEADER,      
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://api.paystack.co/transfer", data=json.dumps(transfer_data), headers=headers)
    except RequestException as e:
        print(e)
    else:
        if response:
            response_dict = response.json()
            if response_dict["data"]["status"] == "success":                
                return response_dict
    return {}


def _post_payment_action(payment, payload, listing):
    paid_at = payload["data"]["paid_at"]

    # Create a pending tenancy waiting for activation
    Tenancy.objects.create(
        tenant=payment.paid_by,
        listing=listing,
        activated=False,        
    )
    payment.date = paid_at
    payment.status = PaymentStatus.COMPLETED
    payment.save()