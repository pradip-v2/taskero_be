from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from taskero_be.core.serializers import ResponseSerializer
from taskero_be.tenants.theme.serializers import TenantThemeSerializer


class TenantViewSet(viewsets.ViewSet):
    @extend_schema(responses={200: TenantThemeSerializer, 404: ResponseSerializer})
    @action(methods=["get"], detail=False, url_path="get-tenant-theme")
    def get_tenant_theme(self, request: Request, *args, **kwargs):
        tenant_theme = request.tenant.tenant_theme
        if not tenant_theme:
            return Response(
                data={"detail": "Theme not set for your tenant"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            data=TenantThemeSerializer(tenant_theme).data,
            status=status.HTTP_200_OK,
        )
