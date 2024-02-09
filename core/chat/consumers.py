from typing import Self

import ujson
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from core.chat import models, utils


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self: Self):
        user = self.scope["user"]
        chat_id = self.scope["path"].split("/")[3]

        if not user.is_authenticated:
            await self.disconnect()

        user_is_participant = await sync_to_async(
            utils.check_user_is_a_participant_of_chat
        )(user, chat_id)
        if not user_is_participant:
            await self.disconnect()

        self.chat_id = chat_id

        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_id, self.channel_name)

    async def receive(self, text_data):
        text_data_json = ujson.loads(text_data)
        body = text_data_json["body"]
        sender = self.scope["user"]

        message = await sync_to_async(models.PrivateTextMessage.objects.create)(
            sender=sender,
            related_chat_id=self.chat_id,
            body=body,
        )

        await self.channel_layer.group_send(
            self.chat_id,
            {
                "type": "chat_message",
                "body": message.body,
                "modified_at": str(message.modified_at.isoformat()),
                "sender": sender.username,
            },
        )

    async def chat_message(self, event):
        body = event["body"]
        sender = event["sender"]
        modified_at = event["modified_at"]

        await self.send(
            text_data=ujson.dumps(
                {
                    "type": "text_message",
                    "body": f"{body}",
                    "sender": f"{sender}",
                    "modified_at": f"{modified_at}",
                }
            )
        )
