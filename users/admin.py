from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from .forms import UserProfileUpdateForm


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileUpdateForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (                      
            'Other Info', # you can also use None 
            {
                'fields': (
                    'user_type',
                    'phone_number',
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
