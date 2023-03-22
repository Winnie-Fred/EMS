from django import forms
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

# Create a UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']

# Create a UserProfileUpdateForm to update image.
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio', 'overview']