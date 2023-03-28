from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Property
from .forms import PropertyFilterForm

# Create your views here.

def property_search(request):
    properties = Property.objects.filter(is_published=True)
    form = PropertyFilterForm(request.GET)
    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        category = form.cleaned_data['category']
        property_type = form.cleaned_data['property_type']
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        min_bedrooms = form.cleaned_data['min_bedrooms']
        max_bedrooms = form.cleaned_data['max_bedrooms']
        min_bathrooms = form.cleaned_data['min_bathrooms']
        max_bathrooms = form.cleaned_data['max_bathrooms']
        min_garage = form.cleaned_data['min_garage']
        max_garage = form.cleaned_data['max_garage']
        min_sqft = form.cleaned_data['min_sqft']
        max_sqft = form.cleaned_data['max_sqft']
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        for_sale_or_rent = form.cleaned_data['for_sale_or_rent']
        
        if search_term:
            properties = properties.filter(Q(title__icontains=search_term) | Q(description__icontains=search_term))
        if category:
            properties = properties.filter(category=category)
        if property_type:
            properties = properties.filter(type=property_type)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if min_bedrooms:
            properties = properties.filter(bedrooms__gte=min_bedrooms)
        if max_bedrooms:
            properties = properties.filter(bedrooms__lte=max_bedrooms)
        if min_bathrooms:
            properties = properties.filter(bathrooms__gte=min_bathrooms)
        if max_bathrooms:
            properties = properties.filter(bathrooms__lte=max_bathrooms)
        if min_garage:
            properties = properties.filter(garage__gte=min_garage)
        if max_garage:
            properties = properties.filter(garage__lte=max_garage)
        if min_sqft:
            properties = properties.filter(sqft__gte=min_sqft)
        if max_sqft:
            properties = properties.filter(sqft__lte=max_sqft)
        if address:
            properties = properties.filter(Q(address__icontains=address) | Q(city__icontains=address) | Q(state__icontains=address))
        if city:
            properties = properties.filter(city__icontains=city)
        if state:
            properties = properties.filter(state__icontains=state)
        if for_sale_or_rent:
            properties = properties.filter(for_sale_or_rent=for_sale_or_rent)
        
        
    context = {
        'properties': properties,
        'form': form,
    }
    
    referrer = request.META.get('HTTP_REFERER')

    if referrer in ['main-site/properties-left-side-bar.html',
                    'main-site/properties-right-side-bar.html',
                    'main-site/properties-list-left-side-bar.html',
                    'main-site/properties-list-right-side-bar.html']:
        return render(request, referrer, context)
    else:
        return render(request, 'main-site/properties-left-side-bar.html', context)


def properties_v1(request):
    return render(request, 'main-site/properties-v1.html')

def properties_v2(request):
    return render(request, 'main-site/properties-v2.html')

@login_required
@user_passes_test(lambda user: not user.userprofile.user_is_tenant)
def add_property(request):
    return render(request, 'main-site/dashboard/add-listing.html')

def properties_left_side_bar(request):
    return render(request, 'main-site/properties-left-side-bar.html')

def properties_right_side_bar(request):
    return render(request, 'main-site/properties-right-side-bar.html')

def properties_list_left_side_bar(request):
    return render(request, 'main-site/properties-list-left-side-bar.html')

def properties_list_right_side_bar(request):
    return render(request, 'main-site/properties-list-right-side-bar.html')

def property_details(request):
    return render(request, 'main-site/properties-details.html')