from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']

    phone_number = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)


# Create a UserProfileUpdateForm to update image.
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio', 'overview']