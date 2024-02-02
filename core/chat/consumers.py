import json
from typing import Self

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.chat import models
from core.chat.permissions import check_user_is_a_participant


class ChatConsumer(WebsocketConsumer):
    def connect(self: Self):
        self.chat_id = self.scope["path"].split("/")[3]
        user = self.scope["user"]
        if not check_user_is_a_participant(user, self.chat_id):
            self.disconnect()

        self.room_group_name = self.chat_id

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

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
