from datetime import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware

from dateutil.relativedelta import relativedelta

class FeeOnPublishedPropertyAndPublishedFeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(listing__is_published=True, is_published=True)
    
# Create your models here.

User = get_user_model()


class Tenancy(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('property.Property', on_delete=models.CASCADE)
    activated = models.BooleanField(help_text="Activate Tenancy")
    start_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Tenancies"
    
    @property
    def rent_or_sale_tenancy(self):
        return self.listing.for_sale_or_rent

    @property
    def rent_due_date(self):
        if self.rent_or_sale_tenancy == 'Rent':
            rent_fee = Fee.published_objects.filter(listing=self.listing, type='rent').first()
            if rent_fee:
                start_date = make_aware(datetime.combine(self.start_date, datetime.min.time()))
                payment_interval = relativedelta(months=1) if rent_fee.recurring == 'monthly' else relativedelta(years=1)
                due_date = start_date + payment_interval
                while due_date < timezone.now():
                    due_date += payment_interval
                return due_date.date()
        return None
    
    @property
    def other_fees_due_date(self):
        fees = Fee.published_objects.filter(tenancy=self.tenancy)
    
    def __str__(self):
        return f"{self.tenant.get_full_name()} Tenancy for {str(self.listing)}"

class Fee(models.Model):
    objects = models.Manager()  # default manager
    published_objects = FeeOnPublishedPropertyAndPublishedFeeManager()  # custom manager

    types = (
        ('paymentForProperty', 'Cost to Purchase or Own Property'),
        ('rent', 'Rent'),
        ('other', 'Other'),
    )

    PROPERTY_TYPES_TO_FEES_TYPE_MAPPING = {
        'Rent':'rent',
        'Sale':'paymentForProperty'
    }

    RECURRENCE_CHOICES = (
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
        ('one-time', 'One-time'),
    )

    listing = models.ForeignKey('property.Property', on_delete=models.CASCADE, null=True, blank=True)
    tenancy = models.ForeignKey(Tenancy, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=18, choices=types)
    name = models.CharField(max_length=255, help_text='e.g. Rent, Property Purchase Cost, Caution Fee, Deposit Fee, Security Fee')
    long_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recurring = models.CharField(max_length=10, choices=RECURRENCE_CHOICES)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    initial_payment_fee = models.BooleanField(help_text="This fee is to be paid on first payment for property e.g. rent, cost to purchase property, deposit fee, caution fee, etc.")
    is_published = models.BooleanField()

    @property
    def short_description(self):
        if self.type == 'rent':
            if self.recurring == 'monthly':
                return 'Monthly Rent'
            elif self.recurring == 'yearly':
                return 'Yearly Rent'
            else:
                return 'Rent'
        elif self.type == 'paymentForProperty':
            return "Property Purchase Cost"
        else:
            return f"{self.recurring.capitalize()} {self.name} fee" if self.recurring else f"One-time {self.name} fee"


    def delete(self, using=None, keep_parents=False):
        self.is_published = False
        self.save()

    def undelete(self):
        self.is_published = True
        self.save()


    def clean(self):
        super().clean()
        if self.listing:
            existing_fees = Fee.published_objects.filter(listing=self.listing, type=self.type)
            if self.pk:
                existing_fees = existing_fees.exclude(pk=self.pk)
            if existing_fees.exists():
                raise ValidationError({'type':f'A fee of type {self.type} has already been placed on this property.'})
            if self.type == 'rent':
                property_fees = Fee.published_objects.filter(listing=self.listing, type='paymentForProperty')
                if property_fees.exists():
                    raise ValidationError({'type':'A paymentForProperty fee has already been placed on this property.'})
            elif self.type == 'paymentForProperty':
                property_fees = Fee.published_objects.filter(listing=self.listing, type='rent')
                if property_fees.exists():
                    raise ValidationError({'type':'A rent fee has already been placed on this property.'})
            if self.type and self.type != "other" and self.type != self.PROPERTY_TYPES_TO_FEES_TYPE_MAPPING.get(self.listing.for_sale_or_rent):
                raise ValidationError({'type':f'A fee of type {self.type} can not be placed on a property of type {self.PROPERTY_TYPES_TO_FEES_TYPE_MAPPING.get(self.listing.for_sale_or_rent)}'})
            if not self.listing and not self.tenancy:
                raise ValidationError('Either a property or tenancy must be selected for this fee.')
            if self.listing and self.tenancy:
                raise ValidationError('A fee can only be placed on either a property or a tenancy, not both.')
            if self.type in ['rent', 'paymentForProperty'] and not self.initial_payment_fee:
                raise ValidationError({'initial_payment_fee':f'A fee of type {self.type} is an initial payment fee and must be set to True'})
            if self.type in ['rent'] and self.recurring not in ['monthly', 'yearly']:
                raise ValidationError({'recurring':f'A fee of type {self.type} must recur either monthly or yearly'})
            if self.type == 'paymentForProperty' and self.recurring != 'one-time':
                raise ValidationError({'recurring':f'A fee of type {self.type} must be a one-time payment fee'})
        elif self.tenancy:
            if self.type in ['rent', 'paymentForProperty']:
                raise ValidationError({'type':f'A rental or purchase fee can only be placed on a property, not a tenancy'})


    def __str__(self):
        return f'{self.short_description} for {self.listing.title or self.tenancy.tenant.full_name}'

class FeePayment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.DO_NOTHING)
    tenancy = models.ForeignKey(Tenancy, on_delete=models.CASCADE)
    payment_date = models.DateField()

    class Meta:
        unique_together = ('fee', 'tenancy')

    def __str__(self):
        if self.fee:
            return f"{str(self.fee)} Fee Payment"
        return f"{str(self.tenancy)} Fee Payment"
        