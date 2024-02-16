from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import direct.routing
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            direct.routing.websocket_urlpatterns
        )
    ),
    'http': get_asgi_application(),  
})