from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()

# Create your views here.

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile':user_profile,
    }
    return render(request, 'main-site/dashboard/profile.html', context)