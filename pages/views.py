from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Count
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required

from property.models import Property, FeaturedProperty
from property.forms import PropertyFilterForm
from helper.views import empty_search_form_context

def get_featured_and_popular_properties():
    form = PropertyFilterForm()
    all_properties = Property.published_objects.all()

    # If the count is less than 5, fetch all properties
    if len(all_properties) < 5:
        popular_properties = all_properties.annotate(num_views=F('number_of_views')).order_by('-num_views')
    else:
        # Otherwise, get the top 5 properties by number of views
        popular_properties = all_properties.annotate(num_views=F('number_of_views')).order_by('-num_views')[:5]    
    
    all_featured_properties = FeaturedProperty.published_objects.filter(is_featured=True, featured_start_date__lte=timezone.now(), featured_end_date__gte=timezone.now())
    featured_sale_properties = all_featured_properties.filter(property__for_sale_or_rent='Sale')
    featured_rent_properties = all_featured_properties.filter(property__for_sale_or_rent='Rent')

    all_featured_properties = [property.property for property in all_featured_properties]
    featured_sale_properties = [property.property for property in featured_sale_properties]
    featured_rent_properties = [property.property for property in featured_rent_properties]

    context = {
        'form':form,
        'popular_properties':popular_properties,
        'featured_sale_properties':featured_sale_properties,
        'featured_rent_properties':featured_rent_properties,
        'all_featured_properties':all_featured_properties,
    }
    return context

# Create your views here.
def home(request):
    return home_01(request)

def home_01(request):
    return render(request, 'main-site/index.html', get_featured_and_popular_properties())

def home_02(request):
    return render(request, 'main-site/index-2.html', get_featured_and_popular_properties())

def home_03(request):    
    return render(request, 'main-site/index-3.html', get_featured_and_popular_properties())

def home_04(request):    
    return render(request, 'main-site/index-4.html', get_featured_and_popular_properties())

def home_05(request):
    return render(request, 'main-site/index-5.html', get_featured_and_popular_properties())

def home_06(request):
    return render(request, 'main-site/index-6.html')

def about(request):
    return render(request, 'main-site/about.html')

def about_v2(request):
    return render(request, 'main-site/about-v2.html')

def service(request):
    return render(request, 'main-site/service.html')

def single_service(request):
    return render(request, 'main-site/single-service.html')

def agency(request):
    return render(request, 'main-site/agency.html')

def create_agency(request):
    return render(request, 'main-site/create-agency.html')

def agent(request):
    return render(request, 'main-site/agent.html')

def agency_details(request):
    return render(request, 'main-site/agency-details.html')

def agent_details(request):
    return render(request, 'main-site/agent-details.html')

def blog_grid(request):
    return render(request, 'main-site/blog-grid.html')

def blog_grid_left_side_bar(request):
    return render(request, 'main-site/blog-grid-left-side-bar.html')

def blog_grid_right_side_bar(request):
    return render(request, 'main-site/blog-grid-right-side-bar.html')

def blog_details(request):
    return render(request, 'main-site/blog-details.html')

@login_required
def dashboard(request):
    return render(request, 'main-site/dashboard/dashboard_index.html')

def map_place_js_view(request):
    context = {'STATIC_URL': settings.STATIC_URL}
    js_string = render_to_string('main-site/js/map-place.js', context=context)
    response = HttpResponse(js_string, content_type='application/javascript')
    return response