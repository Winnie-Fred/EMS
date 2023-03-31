from django import forms

from .models import Property, PropertyExteriorImage, PropertyInteriorImage


class PropertyExteriorImageForm(forms.ModelForm):
    class Meta:
        model = PropertyExteriorImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }


class PropertyInteriorImageForm(forms.ModelForm):
    class Meta:
        model = PropertyInteriorImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class PropertyFilterForm(forms.Form):
    search_term = forms.CharField(required=False, label='Search')
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


    def extract_all_values(self, get_request):
        get_request = get_request.copy()
        for key, value in get_request.items():
            if key in ['min_price', 'max_price', 'min_sqft', 'max_sqft', 'min_bedrooms', 'max_bedrooms', 'min_bathrooms', 'max_bathrooms', 'min_garage', 'max_garage']:
                # remove all non-digit characters from the value
                get_request[key] = ''.join(filter(str.isdigit, value))            
            else:
                get_request[key] = value
        return get_request
        
