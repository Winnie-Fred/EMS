from django.contrib import admin

# Register your models here.
from django.forms import inlineformset_factory

from .models import Tenancy, Fee, FeePayment
from .forms import FeeForm


class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0


class TenancyAdmin(admin.ModelAdmin):
    inlines = [FeeInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, FeeInline):
                # Use inlineformset_factory to create a formset
                # with FeeForm as the form class
                formset = inlineformset_factory(
                    Tenancy, Fee, form=FeeForm, extra=1
                )
                yield formset, inline.instance, inline.inline_related_models

            else:
                yield inline.get_formset(request, obj), inline.instance, inline.inline_related_models


admin.site.register(Tenancy, TenancyAdmin)
admin.site.register(Fee)
admin.site.register(FeePayment)
