"""estateX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views


app_name = 'pages'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home_01/', views.home_01, name='home_01'),
    path('home_02/', views.home_02, name='home_02'),
    path('home_03/', views.home_03, name='home_03'),
    path('home_04/', views.home_04, name='home_04'),
    path('home_05/', views.home_05, name='home_05'),
    path('home_06/', views.home_06, name='home_06'),
    path('about/', views.about, name='about'),
    path('about_v2/', views.about_v2, name='about_v2'),
    path('map_place_js/', views.map_place_js_view, name='map_place_js'),
    path('service/', views.service, name='service'),
    path('single_service/', views.single_service, name='single_service'),
    path('agency/', views.agency, name='agency'),
    path('create_agency/', views.create_agency, name='create_agency'),
    path('agent/', views.agent, name='agent'),
    path('agency_details/', views.agency_details, name='agency_details'),
    path('agent_details/', views.agent_details, name='agent_details'),
    path('blog_grid/', views.blog_grid, name='blog_grid'),
    path('blog_grid_left_side_bar/', views.blog_grid_left_side_bar, name='blog_grid_left_side_bar'),
    path('blog_grid_right_side_bar/', views.blog_grid_right_side_bar, name='blog_grid_right_side_bar'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
