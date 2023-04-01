from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone

from .models import Property, FeaturedProperty
from .forms import PropertyFilterForm

from helper.views import empty_search_form_context
from helper import configurations

def fetch_properties():
    properties = Property.published_objects.all()
    return {'all_properties':properties, 'form':PropertyFilterForm()}

# Create your views here.

def property_search(request):
    properties = Property.published_objects.all()
    form = PropertyFilterForm()
    processed_get_request = form.extract_all_values(request.GET)
    form = PropertyFilterForm(processed_get_request)
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
            properties = properties.annotate(total_price=Sum('fee__amount', filter=(Q(fee__type='paymentForProperty', fee__is_published=True) | Q(fee__type='rent', fee__is_published=True))))
            properties = properties.filter(total_price__gte=min_price)
        if max_price:
            properties = properties.annotate(total_price=Sum('fee__amount', filter=(Q(fee__type='paymentForProperty', fee__is_published=True) | Q(fee__type='rent', fee__is_published=True))))
            properties = properties.filter(total_price__lte=max_price)
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

        print(f"Search successful: Found {len(properties)}", properties)
    else:
        messages.error(request, configurations.ERROR_IN_FORM_MESSAGE)          
    context = {
        'all_properties': properties,
        'form': form,
        'search':True
    }

    return render(request, 'main-site/properties-left-side-bar.html', context)

def properties_v1(request):
    return render(request, 'main-site/properties-v1.html', fetch_properties())

def properties_v2(request):
    all_properties = Property.published_objects.all()
    properties_for_sale = all_properties.filter(for_sale_or_rent='Sale')
    properties_for_rent = all_properties.filter(for_sale_or_rent='Rent')
    context = {
        'all_properties': all_properties,
        'properties_for_sale': properties_for_sale,
        'properties_for_rent': properties_for_rent,
        'form':PropertyFilterForm()
    }
    return render(request, 'main-site/properties-v2.html', context)

@login_required
@user_passes_test(lambda user: not user.userprofile.user_is_tenant)
def add_property(request):
    return render(request, 'main-site/dashboard/add-listing.html')

def properties_left_side_bar(request):   
    all_properties = Property.published_objects.all()
    featured_properties = FeaturedProperty.published_objects.filter(is_featured=True, featured_start_date__lte=timezone.now(), featured_end_date__gte=timezone.now()) 
    featured_properties = [property.property for property in featured_properties]
    context = {'all_properties':all_properties, 'featured_properties':featured_properties, 'form':PropertyFilterForm()}
    return render(request, 'main-site/properties-left-side-bar.html', context)

def properties_right_side_bar(request):    
    return render(request, 'main-site/properties-right-side-bar.html', fetch_properties())

def properties_list_left_side_bar(request):        
    return render(request, 'main-site/properties-list-left-side-bar.html', fetch_properties())

def properties_list_right_side_bar(request):         
    return render(request, 'main-site/properties-list-right-side-bar.html', fetch_properties())

def property_detail(request, pk):  
    property = get_object_or_404(Property, pk=pk) 
    property.number_of_views += 1 
    property.save()

    form = PropertyFilterForm()
    context = {
        'property':property,
        'form': form
    }
    return render(request, 'main-site/properties-details.html', context)

def property_details(request):  
    return render(request, 'main-site/properties-details.html', empty_search_form_context)