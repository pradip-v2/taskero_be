from taskero_be.tenants.models import Domain
from taskero_be.tenants.models import Tenant

# create your public tenant
tenant, _ = Tenant.objects.get_or_create(schema_name="public", name="public")
tenant.save()

# Add one or more domains for the tenant
domain = Domain()
domain.domain = "localhost"  # don't add your port or www here! on a local server you'll want to use localhost here  # noqa: E501
domain.tenant = tenant
domain.is_primary = True
domain.save()
