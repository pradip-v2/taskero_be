from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from taskero_be.communication.routing import websocket_urlpatterns
from taskero_be.tenants.middlewares import JWTAuthMiddleware
from taskero_be.tenants.middlewares import TenantASGIMiddleware

websocket_application = ProtocolTypeRouter(
    {
        "websocket": TenantASGIMiddleware(
            JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
        ),
    },
)
