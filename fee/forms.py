from django import forms

from .models import Fee
from property.models import Property

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = '__all__'