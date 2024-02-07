import json
from typing import Self

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.chat import models, utils


class ChatConsumer(WebsocketConsumer):
    def connect(self: Self):
        user = self.scope["user"]
        chat_id = self.scope["path"].split("/")[3]

        if not user.is_authenticated:
            self.disconnect()

        if not utils.check_user_is_a_participant_of_chat(user, chat_id):
            self.disconnect()

        self.chat_id = chat_id

        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name,
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        sender = self.scope["user"]

        message = models.PrivateTextMessage.objects.create(
            sender=sender,
            related_chat_id=self.chat_id,
            body=body,
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_id,
            {
                "type": "chat_message",
                "body": message.body,
                "modified_at": str(message.modified_at.isoformat()),
                "sender": sender.username,
            },
        )

    def chat_message(self, event):
        body = event["body"]
        sender = event["sender"]
        modified_at = event["modified_at"]

        self.send(
            text_data=json.dumps(
                {
                    "type": "text_message",
                    "body": f"{body}",
                    "sender": f"{sender}",
                    "modified_at": f"{modified_at}",
                }
            )
        )
