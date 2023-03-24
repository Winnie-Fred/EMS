from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.contrib import messages

from allauth.account.views import SignupView, LoginView, LogoutView


from .forms import CustomSignupForm, CustomLoginForm
from helper.configurations import ERROR_IN_FORM_MESSAGE

# Create your views here.

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'main-site/signup.html'
    success_url = reverse_lazy('authentication:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CustomSignupForm(self.request.POST)
        else:
            context['form'] = CustomSignupForm()
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, ERROR_IN_FORM_MESSAGE)
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors, non_field_errors=form.non_field_errors))

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'main-site/login.html'
    success_url = reverse_lazy('pages:home')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
    
        if self.request.POST:
            context['form'] = CustomLoginForm(self.request.POST)
        else:
            context['form'] = CustomLoginForm()
        return context
    
    def form_invalid(self, form):
        messages.error(self.request, ERROR_IN_FORM_MESSAGE)
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors, non_field_errors=form.non_field_errors))
    

class CustomLogoutView(LogoutView):
    template_name = 'main-site/logout.html'