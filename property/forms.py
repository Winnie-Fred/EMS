from django import forms
from django.forms import inlineformset_factory

from .models import Property, PropertyExteriorImage, PropertyInteriorImage

class PropertyExteriorImageForm(forms.ModelForm):
    class Meta:
        model = PropertyExteriorImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class PropertyInteriorImageForm(forms.ModelForm):
    class Meta:
        model = PropertyInteriorImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }


PropertyExteriorImageFormSet = inlineformset_factory(Property, PropertyExteriorImage, form=PropertyExteriorImageForm, extra=1)
PropertyExteriorImageFormSet = inlineformset_factory(Property, PropertyInteriorImage, form=PropertyInteriorImageForm, extra=1)

class PropertyFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search')
    category = forms.ChoiceField(choices=Property.CATEGORY_CHOICES, required=False)
    property_type = forms.ChoiceField(choices=Property.PROPERTY_TYPES, required=False)
    min_price = forms.DecimalField(decimal_places=2, required=False, label='Minimum Price')
    max_price = forms.DecimalField(decimal_places=2, required=False, label='Maximum Price')
    min_bedrooms = forms.IntegerField(required=False, label='Minimum Bedrooms')
    max_bedrooms = forms.IntegerField(required=False, label='Maximum Bedrooms')
    min_bathrooms = forms.IntegerField(required=False, label='Minimum Bathrooms')
    max_bathrooms = forms.IntegerField(required=False, label='Maximum Bathrooms')
    min_garage = forms.IntegerField(required=False, label='Minimum Garage')
    max_garage = forms.IntegerField(required=False, label='Maximum Garage')
    min_sqft = forms.IntegerField(required=False, label='Minimum Square Footage')
    max_sqft = forms.IntegerField(required=False, label='Maximum Square Footage')
    address = forms.CharField(required=False, label='Address')
    city = forms.CharField(required=False, label='City')
    state = forms.CharField(required=False, label='State')
    for_sale_or_rent = forms.ChoiceField(choices=Property.PROPERTY_TYPES, required=False, label='For Sale/Rent')
    is_published = forms.BooleanField(required=False, label='Published')
