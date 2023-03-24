import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


from cloudinary.models import CloudinaryField

from helper import configurations


# Create your models here.

from django.core.exceptions import ValidationError
from django.db import models
import re

class NigerianPhoneNumberField(models.CharField):
    default_validators = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 11)
        kwargs.setdefault('blank', False)
        kwargs.setdefault('unique', True)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value

        value = re.sub('[^0-9]', '', value)  # Remove any non-digit characters
        if len(value) != 10:
            raise ValidationError('Phone number must be exactly 10 digits long.')

        return value

    def get_prep_value(self, value):
        # Add leading zero to the phone number
        return f'0{value}'

    def formfield(self, **kwargs):
        defaults = {'min_length': 10, 'max_length': 10}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    phone_number = NigerianPhoneNumberField()
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('Agent', 'Agent'),
        ('Prospective Tenant', 'Prospective Tenant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=False)

    @property
    def phone_number_formatted(self):
        return f'{self.phone_number[:4]} {self.phone_number[4:7]} {self.phone_number[7:]}'

    
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images', default=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images/default_avatar_sanr5o.png', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())
    bio = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

