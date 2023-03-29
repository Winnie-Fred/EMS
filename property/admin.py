from django.contrib import admin
from django.forms import inlineformset_factory

from fee.forms import FeeForm
from fee.models import Fee
from .models import Property, PropertyExteriorImage, PropertyInteriorImage, FeaturedProperty

# Register your models here.

class FeeInline(admin.TabularInline):
    model = Fee
    extra = 0

class PropertyExteriorImageInline(admin.TabularInline):
    model = PropertyExteriorImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return u'<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            )
        else:
            return '(No image)'

    image_preview.allow_tags = True
    image_preview.short_description = 'Image'


class PropertyInteriorImageInline(admin.TabularInline):
    model = PropertyInteriorImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return u'<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            )
        else:
            return '(No image)'

    image_preview.allow_tags = True
    image_preview.short_description = 'Image'


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
