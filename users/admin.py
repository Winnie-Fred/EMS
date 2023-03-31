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
    list_display = UserAdmin.list_display + ('user_type', 'bank_name', 'account_number')

    def user_type(self, obj):
        return obj.userprofile.user_type

    def bank_name(self, obj):
        return obj.userprofile.bank_name
    
    def account_number(self, obj):
        return obj.userprofile.account_number

    user_type.short_description = 'User Type'
    bank_name.short_description = 'Bank Name'
    account_number.short_description = 'Account Number'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
