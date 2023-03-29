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


app_name = 'property'

urlpatterns = [    
    path('properties_v1/', views.properties_v1, name='properties_v1'),
    path('properties_v2/', views.properties_v2, name='properties_v2'),
    path('add_property/', views.add_property, name='add_property'),
    path('properties_left_side_bar/', views.properties_left_side_bar, name='properties_left_side_bar'),
    path('properties_right_side_bar/', views.properties_right_side_bar, name='properties_right_side_bar'),
    path('properties_list_left_side_bar/', views.properties_list_left_side_bar, name='properties_list_left_side_bar'),
    path('properties_list_right_side_bar/', views.properties_list_right_side_bar, name='properties_list_right_side_bar'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property_details/', views.property_details, name='property_details'),
    path('property_search/', views.property_search, name='property_search'),

    ]
