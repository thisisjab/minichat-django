from typing import Self

import ujson
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from pydantic import ValidationError as PydanticValidationError

from core.chat import models, schemas, utils

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self: Self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.disconnect()

        # Add user to all related private chats (use sync_to_async)
        private_chats = await sync_to_async(list)(user.private_chats.all())
        for private_chat in private_chats:
            await self.channel_layer.group_add(
                str(private_chat.pk),
                self.channel_name,
            )

        # Add user to their private channel
        await self.channel_layer.group_add(
            str(user.pk),
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        for group in self.private_chats_list:
            await self.channel_layer.group_discard(
                group.pk,
                self.channel_name,
            )

    async def receive(self, text_data=None, bytes_data=None):
        received_data = ujson.loads(text_data)
        type = received_data.get("type", None)

        match type:
            case schemas.MessageType.PRIVATE_TEXT_MESSAGE.value:
                await self.handle_private_text_message(received_data)
            case _:
                await self.raise_error("Unsupported message type or invalid request.")

    async def raise_error(self, detail):
        await self.channel_layer.group_send(
            str(self.scope["user"].pk),
            {
                "type": "error",
                "detail": detail,
            },
        )

    async def error(self, event):
        await self.send(text_data=ujson.dumps(event))

    async def handle_private_text_message(self, received_data: dict):
        try:
            data = schemas.PrivateTextMessageSchema(**received_data)
            sender = self.scope["user"]
            receiver = await sync_to_async(models.User.objects.filter)(
                username=data.receiver
            )
            receiver_exists = await sync_to_async(receiver.exists)()

            if not receiver_exists:
                await self.raise_error(f"No user found with username {data.receiver}.")
                return

            receiver = await sync_to_async(receiver.get)(username=data.receiver)

            if sender.username == receiver.username:
                await self.raise_error("Cannot send message to yourself.")
                return

            private_chat = await sync_to_async(utils.get_or_create_private_chat)(
                [sender, receiver]
            )

            message = await sync_to_async(models.PrivateTextMessage.objects.create)(
                sender=sender,
                related_chat_id=private_chat.pk,
                body=data.body,
            )

            await self.channel_layer.group_send(
                str(private_chat.pk),
                {
                    "type": schemas.MessageType.PRIVATE_TEXT_MESSAGE.value,
                    "body": message.body,
                    "sender": sender.username,
                    "receiver": receiver.username,
                    "modified_at": message.modified_at.strftime(DATETIME_FORMAT),
                },
            )

        except PydanticValidationError:
            await self.raise_error(f"Not a valid schema for type `{type}`.")

    async def private_text_message(self, event):
        await self.send(text_data=ujson.dumps(event))
