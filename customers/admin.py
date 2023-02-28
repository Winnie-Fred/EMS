from django.contrib import admin
from django.apps import apps
from tenant_schemas.utils import get_public_schema_name
from .models import Client

# Register your models here.


class TenantsAdmin(admin.ModelAdmin):
    '''
    Hides public models from tenants
    '''
    def has_view_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_add_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_change_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_delete_permission(self,request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
    def has_view_or_change_permission(self, request, view=None):
        if request.tenant.schema_name == get_public_schema_name():
            return True
        else:
            return False
    
app = apps.get_app_config('customers')

# for model_name, model in app.models.items():
#     admin.site.register(model, TenantsAdmin)

admin.site.register(Client, TenantsAdmin)
