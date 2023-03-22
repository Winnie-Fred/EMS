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

    def save(self, *args, **kwargs):
        self.phone_number = '+234' + self.phone_number
        super().save(*args, **kwargs)

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = CloudinaryField('image', folder=f'{configurations.CLOUDINARY_ROOT_DIR}/user_profile_images', default='static/main-site/assets/images/user/default_avatar.png',
                                     transformation={
                                    'width': 62,
                                    'height': 62,
                                    'crop': 'fill',
                                    'radius': 'max',
                                    'gravity': 'auto'
                            })
    bio = models.TextField(blank=True)
    overview = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

