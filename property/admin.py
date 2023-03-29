from django.contrib import admin

from fee.forms import FeeForm
from fee.models import Fee
from .models import Property, PropertyExteriorImage, PropertyInteriorImage, FeaturedProperty

# Register your models here.

class FeeInline(admin.TabularInline):
    model = Fee
    extra = 1

class PropertyExteriorImageInline(admin.TabularInline):
    model = PropertyExteriorImage
    extra = 1


class PropertyInteriorImageInline(admin.TabularInline):
    model = PropertyInteriorImage
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [
        PropertyExteriorImageInline,
        PropertyInteriorImageInline,
        FeeInline,
    ]


admin.site.register(Property, PropertyAdmin)
admin.site.register(FeaturedProperty)
admin.site.register(PropertyExteriorImage)
admin.site.register(PropertyInteriorImage)
