from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


from cloudinary.models import CloudinaryField

from helper import configurations


# Create your models here.

class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('Agent', 'Agent'),
        ('Prospective Tenant', 'Prospective Tenant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=False)

    @property
    def phone_number_formatted(self):
        return '+234' + self.phone_number

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images', default=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images/default_avatar_sanr5o.png')
    bio = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

