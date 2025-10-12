from rest_framework import serializers

from taskero_be.tenants.theme.models import TenantTheme


class TenantThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantTheme
        fields = serializers.ALL_FIELDS
