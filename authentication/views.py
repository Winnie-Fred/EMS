from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages

from allauth.account.views import SignupView, LoginView, LogoutView


from .forms import CustomSignupForm, CustomLoginForm

# Create your views here.
def home(request):
    return render(request, 'main-site/index-6.html')

def map_place_js_view(request):
    context = {'STATIC_URL': settings.STATIC_URL}
    js_string = render_to_string('main-site/js/map-place.js', context=context)
    response = HttpResponse(js_string, content_type='application/javascript')
    return response

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
        print(f"Yes, form is invalid: {self.request.POST}")
        messages.error(self.request, 'Please correct the errors in the form')
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors, non_field_errors=form.non_field_errors))

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'main-site/login.html'
    success_url = reverse_lazy('home')

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect(reverse_lazy('authentication:logout'))
    #     return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
    
        if self.request.POST:
            context['form'] = CustomLoginForm(self.request.POST)
        else:
            context['form'] = CustomLoginForm()
        return context
    
    def form_invalid(self, form):
        print(f"Yes, form is invalid: {form.errors}")
        messages.error(self.request, 'Please correct the errors in the form')
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors, non_field_errors=form.non_field_errors))
    

class CustomLogoutView(LogoutView):
    template_name = 'main-site/logout.html'