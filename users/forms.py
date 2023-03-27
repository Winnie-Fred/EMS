
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .models import UserProfile
from helper.views import fetch_banks

User = get_user_model()

def get_bank_choices():
    bank_choices = cache.get('bank_choices')
    if bank_choices is None:
        bank_choices = fetch_banks()
        cache.set('bank_choices', bank_choices, timeout=60*60*24) # cache for 24 hours
    return bank_choices

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']

    phone_number = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'bio', 'overview', 'bank_name', 'account_number']

    bank_name = forms.ChoiceField(choices=[])
    account_number = forms.CharField(widget=forms.TextInput(), max_length=25, validators=[RegexValidator(r'^\d{1,25}$', 'Enter a valid account number.')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bank_choices = get_bank_choices()
        self.fields['bank_name'].choices = bank_choices
        self.initial['bank_name'] = bank_choices[0][0]
        user_type = self.instance.user.user_type
        if user_type not in ['Prospective Tenant', 'Tenant']:
            for field in self.fields.values():
                field.required = True

    def clean_bank_name(self):
        bank_name_value = self.cleaned_data['bank_name']
        if bank_name_value == '---':
            raise ValidationError("Please select an option.")
        return bank_name_value
    
class UserProfileBankAcctInfoUpdateForm(UserProfileUpdateForm):
    class Meta:
        model = UserProfile
        fields = ['bank_name', 'account_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove all fields except 'bank_name' and 'account_number'
        for field_name in self.fields.copy():
            if field_name not in ['bank_name', 'account_number']:
                del self.fields[field_name]


