from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from taskero_be.tenants.models import Domain
from taskero_be.tenants.models import Tenant
from taskero_be.tenants.theme.models import TenantTheme


@admin.register(Tenant)
class TenantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(TenantTheme)
admin.site.register(Domain)
