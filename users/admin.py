from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
