from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'main-site/index-3.html')

def home_01(request):
    return render(request, 'main-site/index.html')

def home_02(request):
    return render(request, 'main-site/index-2.html')

def home_03(request):
    return render(request, 'main-site/index-3.html')

def home_04(request):
    return render(request, 'main-site/index-4.html')

def home_05(request):
    return render(request, 'main-site/index-5.html')

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