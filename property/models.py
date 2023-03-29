import hashlib

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from cloudinary.models import CloudinaryField

from helper.views import validate_image
from helper import configurations

User = get_user_model()
# Create your models here.

class Property(models.Model):
    class Meta:
        verbose_name_plural = "Properties"

    PROPERTY_TYPES = (
        ('Sale', 'For Sale'),
        ('Rent', 'For Rent'),
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(help_text='Provide detailed description of the property, ideally, not less than 55 words')
    is_published = models.BooleanField(default=True)
    number_of_views = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.title


class FeaturedProperty(models.Model):
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
    image = CloudinaryField('image', validators=[validate_image], folder=f'{configurations.CLOUDINARY_ROOT_DIR}/property_exterior_images', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())


class PropertyInteriorImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = CloudinaryField('image', validators=[validate_image], folder=f'{configurations.CLOUDINARY_ROOT_DIR}/property_interior_images', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())








