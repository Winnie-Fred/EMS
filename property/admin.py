from django.contrib import admin
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.core.exceptions import ValidationError

from property.forms import PropertyInteriorImageForm, PropertyExteriorImageForm
from fee.models import Fee
from .models import Property, PropertyExteriorImage, PropertyInteriorImage, FeaturedProperty

# Register your models here.

class RequiredFeeFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_rent = False
        has_payment_for_property = False
        for form in self.forms:
            if form.cleaned_data.get('type') == 'rent':
                has_rent = True
            elif form.cleaned_data.get('type') == 'paymentForProperty':
                has_payment_for_property = True

        if not has_rent and not has_payment_for_property:
            raise ValidationError('At least one fee of type rent or paymentForProperty is required.')

class FeeInline(admin.StackedInline):
    model = Fee
    extra = 1
    formset = RequiredFeeFormSet


class PropertyExteriorImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Check if at least one image field is filled
        has_image = False
        for form in self.forms:
            if form.cleaned_data.get('image'):
                has_image = True
                break

        if not has_image:
            raise ValidationError('At least one image is required for exterior images.')
    
        

class PropertyExteriorImageInline(admin.TabularInline):
    model = PropertyExteriorImage
    extra = 1
    formset = PropertyExteriorImageFormSet
    min_num=1
    max_num=10
    validate_min=True

class PropertyInteriorImageFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Check if at least one image field is filled
        has_image = False
        for form in self.forms:
            if form.cleaned_data.get('image'):
                has_image = True
                break

        if not has_image:
            raise ValidationError('At least one image is required for exterior images.')


class PropertyInteriorImageInline(admin.TabularInline):
    model = PropertyInteriorImage
    extra = 1
    formset = PropertyInteriorImageFormSet
    min_num=1
    max_num=10
    validate_min=True


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
