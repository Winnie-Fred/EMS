
from django.urls import path
from . import views


app_name = 'fee'

urlpatterns = [    
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('property_payment_success/', views.property_payment_success, name='property_payment_success'),
    path('property_payment_failed/', views.property_payment_failed, name='property_payment_failed'),
    path('property_payment_init/', views.property_payment_init, name='property_payment_init'),
    ]
