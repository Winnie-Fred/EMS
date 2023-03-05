from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from tenant_schemas.utils import get_tenant_model, schema_context


class Command(BaseCommand):
    help = 'Create a site object for each tenant.'

    def handle(self, *args, **options):
        TenantModel = get_tenant_model()

        for tenant in TenantModel.objects.all():
            # Set the schema name for this tenant
            schema_name = tenant.schema_name

            # Switch to the tenant schema
            with schema_context(schema_name):
                site = Site.objects.create(
                    domain=tenant.domain_url,
                    name=tenant.schema_name,
                )

            self.stdout.write(self.style.SUCCESS(f'Successfully created site "{site}" for tenant "{tenant}"'))

