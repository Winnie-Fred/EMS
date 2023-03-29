from django.contrib import admin

# Register your models here.

from .models import Tenancy, Fee, FeePayment
from .forms import FeeForm


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0


class TenancyAdmin(admin.ModelAdmin):
    inlines = [FeeInline]

class FeeAdmin(admin.ModelAdmin):
    form = FeeForm


admin.site.register(Tenancy, TenancyAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(FeePayment)
