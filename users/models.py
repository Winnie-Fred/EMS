import re
import hashlib

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


from cloudinary.models import CloudinaryField

from helper import configurations


# Create your models here.


class NigerianPhoneNumberField(models.CharField):
    default_validators = []

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 10)
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


    def formfield(self, **kwargs):
        defaults = {'min_length': 10, 'max_length': 10}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    # phone_number = NigerianPhoneNumberField()
    phone_number = models.CharField(max_length=10, blank=False, unique=True)
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('Agent', 'Agent'),
        ('Prospective Tenant', 'Prospective Tenant'),
        ('Tenant', 'Tenant'),
        ('Estate Manager', 'Estate Manager'),
        ('Estate Staff Member', 'Estate Staff Member'),
    )
    user_type = models.CharField(max_length=19, choices=USER_TYPE_CHOICES, blank=False)

    @property
    def phone_number_formatted(self):
        return f'0{self.phone_number[:3]} {self.phone_number[3:6]} {self.phone_number[6:]}'

    @property
    def phone_number_raw(self):
        return f'0{self.phone_number}'
    

    
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images', default=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images/default_avatar_sanr5o.png', public_id=lambda instance: hashlib.sha256(instance.image.read()).hexdigest())
    bio = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    bank_name = models.CharField(max_length=50, blank=True)
    account_number = models.CharField(max_length=25, blank=True, validators=[RegexValidator(r'^\d{1,25}$', 'Enter a valid account number.')])


    @property
    def user_role(self):
        if self.user.user_type:
            return self.user.user_type
        else:
            if self.user.is_superuser:
                return "Estate Manager"
            elif self.user.is_staff:
                return "Estate Staff Member"
            else:
                return ""
        
    @property
    def user_is_tenant(self):
        return self.user.user_type in ['Prospective Tenant', 'Tenant']

    def __str__(self):
        return f'{self.user.username} Profile'

