from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import UserUpdateForm, UserProfileUpdateForm
from helper.configurations import ERROR_IN_FORM_MESSAGE

User = get_user_model()

# Create your views here.

@login_required
def profile(request):
   
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if 'profile_pic_edit_btn' in request.POST:
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Your profile picture has been updated!')                
                return redirect('users:profile')
            else:
                messages.error(request, ERROR_IN_FORM_MESSAGE)                
        elif 'profile_edit_btn' in request.POST:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')                
                return redirect('users:profile')
            else:
                messages.error(request, ERROR_IN_FORM_MESSAGE)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main-site/dashboard/profile.html', context)