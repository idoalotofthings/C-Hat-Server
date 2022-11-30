"""
ASGI config for c_hat_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routing
from busprovider import bus
import signal
import sys

def stop(_, __):
    bus.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, stop)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c_hat_server.settings')

application = ProtocolTypeRouter({
    'http': AsgiHandler(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
