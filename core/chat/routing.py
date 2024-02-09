from django.urls import path, re_path

from core.chat import consumers

ws_urlpatterns = [
    re_path(
        r"^ws/chat/(?P<id>[0-9a-f-]+)/$",
        consumers.ChatConsumer.as_asgi(),
        name="chat",
    ),
    path(
        "ws/channel/",
        consumers.ChannelConsumer.as_asgi(),
        name="channel",
    ),
]
