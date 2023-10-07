import json
import logging

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .utils import generate_unique_reference, initialize_payment, verify_payment, _post_payment_action, SAAS_PERCENTAGE_CHARGE_PROPERTY
from property.models import Property
from .models import FeePayment, PaymentStatus

User = get_user_model()
logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def property_payment_init(request):

    if request.method == 'POST':                    
        property_id = request.POST.get('property_id')
        property = get_object_or_404(Property, id=property_id)

        if not request.user.userprofile.user_is_tenant:
            messages.error(request, "Only tenants or prospective tenants can make payments for property.")
            return redirect('property:property_detail', property_id)
        

        if property.is_occupied_by is not None or property.tenancy_awaiting_activation:
            messages.error(request, "This property is currently off the market because it is occupied or has been paid for")
            return redirect('property:property_detail', property_id)
        

        amount = property.price

        callback_url = request.build_absolute_uri(
            reverse('fee:payment_callback'))
        failure_url = request.build_absolute_uri(
            reverse('fee:property_payment_failed'))

        # Initialize unprocessed payment to get reference for tracking payment
        payment = FeePayment(
            paid_by=request.user,
            paid_to=property.listed_by,
            amount=amount,
            saas_percentage_charge=SAAS_PERCENTAGE_CHARGE_PROPERTY,
        )
        payment.reference = generate_unique_reference(
            payment, char_length=8)
        fees_data = []
        for fee in property.initial_payment_fees:
            fee_data = {
                'id': fee.id,
                'listing_id': fee.listing.id if fee.listing else None,
                'tenancy_id': fee.tenancy.id if fee.tenancy else None,
                'type': fee.type,
                'name': fee.name,
                'long_description': fee.long_description,
                'short_description':fee.short_description,
                'amount': str(fee.amount),
                'recurring': fee.recurring,
                'due_date': fee.due_date.isoformat() if fee.due_date else None,
                'created_at': fee.created_at.isoformat(),
                'initial_payment_fee': fee.initial_payment_fee,
                'is_published': fee.is_published,
            }
            fees_data.append(fee_data)
        fees_snapshot = json.dumps(fees_data)
        payment.fees_snapshot = fees_snapshot
        payment.save()

        for fee in property.initial_payment_fees:
            payment.fees.add(fee)

        payment.save()

        # metadata to pass additional data that 
        # the endpoint doesn't accept naturally.
        metadata= json.dumps({"payment_id":payment.pk,  
                                "cancel_action":failure_url,  
                                "property_id":property.pk,
                            })

        payment_url = initialize_payment(
            request.user.email, amount, payment.reference, metadata, callback_url)
        if payment_url:
            return redirect(payment_url, code=303)
        else:       
            return redirect(reverse('fee:property_payment_failed'))
    return redirect('property:properties_v2')

def property_payment_success(request):    
    return render(request, 'main-site/payment-success.html')

def property_payment_failed(request):
    context = {
        'details': "Oops! Something went wrong. You can try checking your internet connection. Please try again later."
    }
    return render(request, 'main-site/payment-failed.html', context)

@login_required
def payment_callback(request):
    '''
    Callback from the paystack payment page.

    Expected in request.GET dict - reference and/or trxref (both are the same)
    '''
    reference = request.GET.get("reference") or request.GET.get("trxref")
    payload = verify_payment(reference)

    if payload:
        try:
            payment = FeePayment.objects.get(reference=reference)
            if payment.status == PaymentStatus.UNPROCESSED:
                logger.info("Processing payment via callback")
                property_id = payload['data']['metadata']['property_id']
                listing = get_object_or_404(Property, id=property_id)
                _post_payment_action(payment, payload, listing)
                context = {'msg':f'Your payment for {listing.title} was successful', 
                           'details':'Your tenancy is undergoing processing. You will be notified immediately your tenancy is activated.'
                           }
            else:
                logger.info("payment_callback - payment already completed")
                context = {'msg':'Payment already completed', 'details':'This payment has already been processed'}
            return render(request, 'main-site/payment-success.html', context)

        except FeePayment.DoesNotExist:
            logger.error(
                "payment_callback - payment does not exist")
            messages.error(request, "Payment does not exist.")
    else:
        messages.error(request, "Unable to verify payment.")
    
    return redirect('property:properties_v2')