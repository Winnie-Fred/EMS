import datetime
from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware


from property.models import Property

# Create your models here.

User = get_user_model()


class Tenancy(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Property, on_delete=models.CASCADE)
    activated = models.BooleanField(help_text="Activate Tenancy")
    start_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Tenancies"
    
    @property
    def rent_or_sale_tenancy(self):
        return self.property.for_sale_or_rent

    @property
    def due_date(self):
        if self.rent_or_sale_tenancy == 'Rent':
            rent_fee = Fee.objects.filter(property=self.property, type='rent').first()
            if rent_fee:
                start_date = make_aware(datetime.combine(self.start_date, datetime.min.time()))
                payment_interval = relativedelta(months=1) if rent_fee.recurring == 'monthly' else relativedelta(years=1)
                due_date = start_date + payment_interval
                while due_date < timezone.now():
                    due_date += payment_interval
                return due_date.date()
        return None

class Fee(models.Model):
    FEE_TYPES = (
        ('rent', 'Rent'),
        ('other', 'Other'),
    )

    RECURRENCE_CHOICES = (
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
        ('one-time', 'One-time'),
    )

    listing = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    tenancy = models.ForeignKey(Tenancy, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=10, choices=FEE_TYPES)
    name = models.CharField(max_length=255)
    long_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recurring = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, blank=True)
    due_date = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    initial_payment_field = models.BooleanField(help_text="This fee is to be paid on first payment for property e.g. rent, deposit fee, caution fee, etc.", default=False)
    is_published = models.BooleanField(default=False)

    @property
    def short_description(self):
        if self.type == 'rent':
            if self.recurring == 'monthly':
                return 'Monthly Rent'
            elif self.recurring == 'yearly':
                return 'Yearly Rent'
            else:
                return 'Rent'
        else:
            return f"{self.recurring.capitalize()} {self.name} fee" if self.recurring else f"One-time {self.name} fee"

    def clean(self):
        if not self.listing and not self.tenancy:
            raise ValidationError('Either a property or tenancy must be selected.')
        if self.listing and self.tenancy:
            raise ValidationError('Only one of property or tenancy can be selected.')

    def __str__(self):
        return f'{self.short_description} for {self.property or self.tenancy}'

class FeePayment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)
    tenancy = models.ForeignKey(Tenancy, on_delete=models.CASCADE)
    payment_date = models.DateField()

    class Meta:
        unique_together = ('fee', 'tenancy')