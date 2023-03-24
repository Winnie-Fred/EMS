from django.db.models.signals import post_save #  Import a post_save signal when a user is created
from django.contrib.auth import get_user_model #  Import the User model, which is a sender
from django.dispatch import receiver #  Import the receiver
from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)