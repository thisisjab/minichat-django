from django.urls import path

from core.chat import consumers

ws_urlpatterns = [
    path(
        "ws/socket/",
        consumers.WSConsumer.as_asgi(),
        name="socket",
    ),
]
