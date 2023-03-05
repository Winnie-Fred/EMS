from customers.models import Client

Client.objects.create(domain_url='estatex.local', schema_name='public', name='EstateX', paid_until='2024-12-31', on_trial=False)

Client.objects.create(domain_url='ngozika.estatex.local', schema_name='ngozika', name='Ngozika Housing Estate', paid_until='2024-12-31', on_trial=True)

Client.objects.create(domain_url='udoka.estatex.local', schema_name='udoka', name='Udoka Housing Estate', paid_until='2024-12-31', on_trial=True)
