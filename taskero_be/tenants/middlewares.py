from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django_tenants.utils import get_public_schema_name
from django_tenants.utils import schema_context
from rest_framework_simplejwt.tokens import AccessToken

from taskero_be.tenants.models import Domain


class TenantASGIMiddleware:
    """
    A middleware to detect the tenant from the host for WebSocket connections.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = scope.get("headers", [])
        host_header = None
        for header in headers:
            if header[0] == b"host":
                host_header = header[1].decode()
                break

        if not host_header:
            return await self.inner(scope, receive, send)

        hostname = host_header.split(":")[0]
        tenant = None

        try:
            tenant = await self.get_tenant_async(hostname)
        except Exception:  # noqa: BLE001
            with schema_context(get_public_schema_name()):
                pass

        if tenant:
            scope["tenant"] = tenant
            scope["schema_name"] = tenant.schema_name

        return await self.inner(scope, receive, send)

    @staticmethod
    @database_sync_to_async
    def get_tenant_async(hostname):
        tenant = None
        try:
            domain = Domain.objects.get(domain=hostname)
            tenant = domain.tenant
        except Exception:  # noqa: BLE001
            # fallback to public schema
            with schema_context(get_public_schema_name()):
                pass
        return tenant


User = get_user_model()


@database_sync_to_async
def get_user(validated_token, scope):
    try:
        with schema_context(scope["schema_name"]):
            user = User.objects.get(id=validated_token["user_id"])
            return user or AnonymousUser()
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that authenticates WebSocket connections using JWT tokens.
    """

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = None

        # Extract token from query params (e.g. ?token=<jwt>)
        if "token=" in query_string:
            token = query_string.split("token=")[-1].split("&")[0]

        if token:
            try:
                validated_token = AccessToken(token)
                scope["user"] = await get_user(validated_token, scope)
            except Exception:  # noqa: BLE001
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
