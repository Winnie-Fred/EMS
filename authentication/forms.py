from django import forms
from allauth.account.forms import SignupForm, LoginForm

class CustomSignupForm(SignupForm):

    terms_accepted = forms.BooleanField()

    def signup(self, request, user):
        pass

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        
        user.save()
        # You must return the original result.
        return user


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(CustomLoginForm, self).login(*args, **kwargs)