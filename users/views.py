import requests
import os
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from dotenv import load_dotenv

from .forms import UserUpdateForm, TenantUserProfileUpdateForm, UserProfileUpdateForm, UserProfileBankAcctInfoUpdateForm
from helper.configurations import ERROR_IN_FORM_MESSAGE

User = get_user_model()
load_dotenv()
    
# Create your views here.

def verify(account_number, bank_name, bank_code):
    print("Making new request...")
    headers = {'Authorization': f'Bearer {os.getenv("PAYSTACK_SECRET_KEY", "paystack_secret_key")}'}
    
    # Verify account details
    url = f'https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}'
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['status']:
        acct_owner_or_error_msg = result['data']['account_name']
    else:
        acct_owner_or_error_msg = result['message']
    return (result['status'], acct_owner_or_error_msg)
        
def verify_account_number(request):
    bank_acct_update_form = UserProfileBankAcctInfoUpdateForm(request.POST, instance=request.user.userprofile)
    if bank_acct_update_form.is_valid():
        account_number = bank_acct_update_form.cleaned_data['account_number']
        bank_name = bank_acct_update_form.cleaned_data['bank_name']
        bank_name, bank_code = bank_name.split('---')
        
        print(account_number, bank_name)
        if 'acct_number' in request.session and 'bank_name' in request.session:
            if request.session['acct_number'] == account_number and request.session['bank_name'] == bank_name:
                print("Nothing has changed")
                return JsonResponse(request.session['response_data'])
        try:
            status, acct_owner_or_error_msg = verify(account_number, bank_name, bank_code)
        except requests.exceptions.RequestException as e:
            error_msg = f"An error occurred while making the request: {e}"
            response_data = JsonResponse({'status':False, 'status_msg':error_msg, 'error_type': 'error_during_request'})
            return response_data
        else:
            if status:
                response_data = JsonResponse({'status':status, 'account_owner': acct_owner_or_error_msg, 'status_msg':"Account Verification successful"})
            else:
                response_data = JsonResponse({'status':status, 'status_msg': acct_owner_or_error_msg, 'error_type': 'acct_info_incorrect'})
            request.session['acct_number'] = account_number
            request.session['bank_name'] = bank_name
            request.session['response_data'] = json.loads(response_data.content)
            return response_data
    else:        
        response_data = JsonResponse({'status':False, 'status_msg': "Please check the form for errors", 'error_type':'form_invalid', "form_errors":bank_acct_update_form.errors})
        return response_data


@login_required
def profile(request):
    context = {}
    
    bank_acct_update_form = not request.user.userprofile.user_is_tenant 

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if bank_acct_update_form:
            p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        else:
            p_form = TenantUserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():            
            if bank_acct_update_form:
                verification = verify_account_number(request)
                verification_data = json.loads(verification.content)
                if verification_data['status']:
                    u_form.save()
                    p_form.save()
                    messages.success(request, 'Your profile has been updated!')                
                    return redirect('users:profile')
                else:
                    error_type = verification_data['error_type']
                    
                    if error_type == 'form_invalid':
                        form_errors = verification_data['form_errors']
                        for field, errors in form_errors.items():
                            for error in errors:
                                p_form.add_error(field, error)
                    messages.error(request, verification_data['status_msg'])
            else:
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')                
                return redirect('users:profile')
        else:
            print(u_form.errors or p_form.errors)
            messages.error(request, ERROR_IN_FORM_MESSAGE)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)
        

    context['u_form'] = u_form
    context['p_form'] = p_form
    context['bank_acct_update_form'] = bank_acct_update_form

    return render(request, 'main-site/dashboard/profile.html', context)