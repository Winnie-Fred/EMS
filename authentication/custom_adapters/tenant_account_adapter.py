from allauth.account.adapter import DefaultAccountAdapter
from tenant_schemas.utils import schema_context

class TenantAccountAdapter(DefaultAccountAdapter):    

    def save_user(self, request, user, form, commit=True):
        # Set the schema name for the current tenant
        schema_name = request.tenant.schema_name

        # Switch to the tenant schema
        with schema_context(schema_name):
            # Call the parent class method to save the user
            return super().save_user(request, user, form, commit=commit)

    def get_login_redirect_url(self, request):
        # Set the schema name for the current tenant
        schema_name = request.tenant.schema_name
        print("USING THIS >>>>>>>>>>>>>>>>>>>>")

        # Switch to the tenant schema
        with schema_context(schema_name):
            # Call the parent class method to get the login redirect URL
            return super().get_login_redirect_url(request)

    def get_email_confirmation_url(self, request, emailconfirmation):
        # Set the schema name for the current tenant
        schema_name = request.tenant.schema_name

        # Switch to the tenant schema
        with schema_context(schema_name):
            # Call the parent class method to get the email confirmation URL
            return super().get_email_confirmation_url(request, emailconfirmation)
