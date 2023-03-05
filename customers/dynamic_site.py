from tenant_schemas.middleware import TenantMiddleware
from django.contrib.sites.models import Site
from django.conf import settings

class DynamicSiteMiddleware(TenantMiddleware):
    def process_request(self, request):
        super().process_request(request)
        domain = request.tenant.domain_url.split(':')[0]
        site = Site.objects.get(domain=domain)
        settings.SITE_ID = site.id
