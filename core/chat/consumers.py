from typing import Self

import ujson
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from pydantic import ValidationError as PydanticValidationError

from core.chat import models, schemas, utils

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"


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


class ChannelConsumer(AsyncWebsocketConsumer):
    """This consumer serves all type of communication including chatting, notifications, etc."""

    async def connect(self: Self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.disconnect()

        self.user_channel_key = utils.create_user_channel_key(user.username)

        await self.channel_layer.group_add(
            self.user_channel_key,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_channel_key, self.channel_name)

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
            self.user_channel_key,
            {
                "type": "error",
                "detail": detail,
            },
        )

    async def error(self, event):
        await self.send(text_data=ujson.dumps(event))

    async def private_text_message(self, event):
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

            private_chat = await sync_to_async(utils.get_or_create_private_chat)(
                [sender, receiver]
            )

            message = await sync_to_async(models.PrivateTextMessage.objects.create)(
                sender=sender,
                related_chat_id=private_chat.pk,
                body=data.body,
            )

            await self.channel_layer.group_send(
                utils.create_user_channel_key(receiver),
                {
                    "type": schemas.MessageType.PRIVATE_TEXT_MESSAGE.value,
                    "body": message.body,
                    "sender": sender.username,
                    "modified_at": message.modified_at.strftime(DATETIME_FORMAT),
                },
            )

        except PydanticValidationError:
            await self.raise_error(f"Not a valid schema for type `{type}`.")
