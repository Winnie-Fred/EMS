from django.shortcuts import render

# Create your views here.
def profile(request):
    return render(request, 'main-site/dashboard/profile.html')