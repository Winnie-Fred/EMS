from django import forms

from .models import Fee
from property.models import Property

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = '__all__'
        

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['property'].queryset = Property.objects.filter(listed_by=user)