import requests
import os

from django.shortcuts import render
from django.core.exceptions import ValidationError

from cloudinary.models import CloudinaryResource
from property.forms import PropertyFilterForm


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

def validate_image(file):
    try:
        if not file.content_type.startswith('image'):
            print("It is not an image")
            raise ValidationError('File is not an image')
    except AttributeError:
        pass

    if not isinstance(file, CloudinaryResource) and file.resource_type == 'image':
        raise ValidationError('File is not an image')

def get_empty_search_form_context():
    return {'form':PropertyFilterForm()}

empty_search_form_context = get_empty_search_form_context()
