import decimal
from datetime import datetime
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models.functions import ExtractDay
from django.db.models import Q, F, OuterRef, Subquery, Count


from fee.models import Fee, Tenancy, FeePayment
from property.models import Property


# Create your views here.
@login_required
def index(request):
    return render(request, 'main-site/dashboard/dashboard_index.html')


@login_required
@user_passes_test(lambda user: user.userprofile.user_is_tenant)
def payments_tenant(request):
    one_month_from_now = make_aware(datetime.now() + timedelta(days=30))
    current_user = request.user

    occupied_properties = Property.objects.annotate(
        current_tenant=Subquery(
            Tenancy.objects.filter(
                listing=OuterRef('pk'),
                activated=True,
                cancelled=False
            ).values('tenant')
        )
    ).filter(current_tenant=current_user)

    fees_due_soon = Fee.published_objects.filter(
        Q(due_date__lte=one_month_from_now),
        Q(tenancy__tenant=current_user) | Q(listing__in=occupied_properties)
    ).annotate(
        days_left=ExtractDay(F('due_date') - make_aware(datetime.now()))
    ).order_by('due_date')

    pending_tenancies = Tenancy.pending_tenancies.filter(tenant=current_user)
    activated_tenancies = Tenancy.activated_tenancies.filter(tenant=current_user)

    fee_payments = FeePayment.objects.filter(paid_by=current_user)
    fees_paid = []
    for fee_payment in fee_payments:
        fees_snapshot = fee_payment.get_fees_snapshot()
        for fee in fees_snapshot:
            fee['amount'] = decimal.Decimal(fee['amount'])
            fee['created_at'] = datetime.fromisoformat(fee['created_at'])
        fees_paid.extend(fees_snapshot)


    context = {
        'fees_due_soon':fees_due_soon,
        'pending_tenancies':pending_tenancies,
        'activated_tenancies':activated_tenancies,
        'fees_paid':fees_paid,

    }
    return render(request, 'main-site/dashboard/payments_tenant.html', context)

def get_fees_snapshot_str(fees_snapshot, payment):
    fees_data = fees_snapshot
    fees_str_list = [fee.get('name') for fee in fees_data]
    fees_str = ", ".join(fees_str_list)
    return f"Fee Payment for {fees_str} by {payment.paid_by.get_full_name()} to {payment.paid_to.get_full_name()}"

@login_required
@user_passes_test(lambda user: user.userprofile.user_role == 'Agent' or user.userprofile.user_role == 'Owner')
def payments_agent_or_owner(request):
    current_user = request.user
    fees_payments = FeePayment.objects.filter(paid_to=current_user)

    total_income = sum(fp.amount_paid_to_property_lister for fp in fees_payments)
    number_of_properties_listed = Property.objects.filter(listed_by=current_user).count()

    listed_properties = Property.objects.filter(listed_by=current_user)
    number_of_properties_listed = len(listed_properties)
    occupied_properties_count = 0
    properties_managed = []
    for listing in listed_properties:
        if listing.is_occupied_by:
            properties_managed.append(listing)
            occupied_properties_count += 1

    fees_received = fees_payments

    context = {
        'total_income': total_income,
        'number_of_properties_listed':number_of_properties_listed,
        'occupied_properties_count':occupied_properties_count,
        'fees_received':fees_received,
        'properties_managed':properties_managed,
    }
    return render(request, 'main-site/dashboard/payments_agent_or_owner.html', context)

