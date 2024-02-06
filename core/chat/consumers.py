import json
from typing import Self

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.chat import models


class ChatConsumer(WebsocketConsumer):
    def connect(self: Self):
        ...

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        sender = self.scope["user"]

        message = models.TextMessage.objects.create(
            sender=sender,
            chat_id=self.chat_id,
            body=body,
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "body": message.body,
                "creation_at": str(message.created_at),
                "sender": sender.username,
            },
        )

    def chat_message(self, event):
        body = event["body"]
        sender = event["sender"]
        creation_at = event["creation_at"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "text_message",
                    "body": f"{body}",
                    "sender": f"{sender}",
                    "created_at": f"{creation_at}",
                }
            )
        )
