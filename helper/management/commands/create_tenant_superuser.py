import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

from tenant_schemas.utils import schema_context
from tenant_schemas.utils import get_tenant_model

from dotenv import load_dotenv
load_dotenv()

class Command(BaseCommand):
    help = 'Creates a superuser for each tenant schema.'

    def handle(self, *args, **options):
        # Get the tenant model
        TenantModel = get_tenant_model()

        for tenant in TenantModel.objects.all():
            # Set the schema name for this tenant
            schema_name = tenant.schema_name

            # Switch to the tenant schema
            with schema_context(schema_name):
                # Create the superuser for this tenant
                User = get_user_model()
                User.objects.create_superuser(
                    username=tenant.name,
                    email=tenant.name+"@gmail.com",
                    password=os.getenv('TENANT_SUPERUSER_PASSWORD', 'password123')
                )

                self.stdout.write(self.style.SUCCESS(
                    f'Successfully created superuser for tenant {tenant.name}.'
                ))