from django.core.management.base import BaseCommand
from customers.models import Client

class Command(BaseCommand):
    help = 'Create 3 tenants.'

    def handle(self, *args, **options):
        Client.objects.create(domain_url='estatex.local', schema_name='public', name='EstateX', paid_until='2024-12-31', on_trial=False)

        Client.objects.create(domain_url='ngozika.estatex.local', schema_name='ngozika', name='Ngozika Housing Estate', paid_until='2024-12-31', on_trial=True)

        Client.objects.create(domain_url='udoka.estatex.local', schema_name='udoka', name='Udoka Housing Estate', paid_until='2024-12-31', on_trial=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully created 3 tenants'))
