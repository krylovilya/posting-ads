import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from apps.main.consumer import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("chat/", ChatConsumer.as_asgi()),
        ])
    ),
})
