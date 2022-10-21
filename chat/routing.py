from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'chat', consumers.ChatServiceConsumer.as_asgi()),
    re_path(r'register', consumers.RegisterUserConsumer.as_asgi())
]