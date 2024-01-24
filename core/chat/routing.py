from django.urls import re_path

from core.chat import consumers

ws_urlpatterns = [
    re_path(
        "ws/socket-server/",
        consumers.ChatConsumer.as_asgi(),
        name="socket-server",
    )
]
