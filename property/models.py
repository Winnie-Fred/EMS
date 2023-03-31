import hashlib

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum, Exists, OuterRef, Subquery
from django.db.models import BooleanField, Case, When

from cloudinary.models import CloudinaryField
from fee.models import Fee

from helper import configurations

class PublishedPropertyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class FeaturedPublishedPropertyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(property__is_published=True)

User = get_user_model()

# Create your models here.

class Property(models.Model):
    objects = models.Manager()  # default manager
    published_objects = PublishedPropertyManager()  # custom manager

    class Meta:
        verbose_name_plural = "Properties"    

    PROPERTY_TYPES = (
        ('Rent', 'For Rent'),
        ('Sale', 'For Sale'),
    )
    CATEGORY_CHOICES = (
        ('RES', 'Residential'),
        ('COM', 'Commercial'),
        ('LUX', 'Luxury'),
    )
    listed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    for_sale_or_rent = models.CharField(max_length=4, choices=PROPERTY_TYPES)
    type = models.CharField(max_length=50, help_text='Type e.g. Apartment, Office')
    date_listed = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    sqft = models.IntegerField(help_text='square footage')
    bedrooms= models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    description = models.TextField(help_text='Provide detailed description of the property, ideally, not less than 55 words')
    is_published = models.BooleanField(default=True)
    number_of_views = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.title

    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state}"

    @property
    def rental_or_purchase_price(self):
        # Get the related fees where type is paymentForProperty or rent
        fees = self.fee_set.filter(type__in=['paymentForProperty', 'rent'], is_published=True)
        # Sum the amounts of the related fees
        total_price = fees.aggregate(Sum('amount'))['amount__sum']
        return total_price if total_price else 0

    @property
    def initial_payment_fees(self):
        return self.fee_set.filter(initial_payment_fee=True, is_published=True)

    @property
    def price(self):
        fees = self.initial_payment_fees
        total_price = fees.aggregate(Sum('amount'))['amount__sum']
        return total_price if total_price else 0
    
    @property
    def rent_fee_recurring_value(self):
        try:
            rent_fee = self.fee_set.get(type='rent')            
        except Fee.DoesNotExist:
            return ''
        else:
            recurring = rent_fee.recurring
            if recurring == 'monthly':
                return 'month'
            elif recurring == 'yearly':
                return 'year'


class FeaturedProperty(models.Model):
    objects = models.Manager()  # default manager
    published_objects = FeaturedPublishedPropertyManager()  # custom manager
    
    class Meta:
        verbose_name_plural = "Featured Properties"
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    featured_start_date = models.DateTimeField(null=True, blank=True)
    featured_end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.property.title

    def update_featured_status(self):
        if self.is_featured and self.featured_end_date and self.featured_end_date <= timezone.now():
            self.is_featured = False
            self.save()


class PropertyExteriorImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/property_exterior_images', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())
            

class PropertyInteriorImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/property_interior_images', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())






