from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignupForm(SignupForm):

    terms_accepted = forms.BooleanField()
    phone_number = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    USER_TYPE_CHOICES = (
        ('Owner', 'Owner'),
        ('Agent', 'Agent'),
        ('Prospective Tenant', 'Prospective Tenant'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, initial="Prospective Tenant")

    def signup(self, request, user):
        pass

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.save()
        # You must return the original result.
        return user


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(CustomLoginForm, self).login(*args, **kwargs)