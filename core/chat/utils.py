from typing import List

from django.contrib.auth import get_user_model

from core.chat import models

User = get_user_model()


def get_last_messages_for_user(user: User):
    """Get last message of all conversations that a user is involved."""
    last_messages = []

    for chat in user.private_chats.all():
        last_message = chat.messages.all().order_by("modified_at").last()
        if last_message:
            last_messages.append(
                {
                    "body": last_message.body,
                    "modified_at": last_message.modified_at,
                    "user": last_message.related_chat.participants.exclude(
                        pk=last_message.sender.pk
                    ).first(),
                }
            )

    return last_messages


def check_if_chat_exists_for_participants(participants: List[User]) -> bool:
    """Checks if a chat with given participants exists.

    Args:
        participants (List[User]): a list of `User` objects

    Returns:
        bool: True if there is a chat with given participants
    """
    existing_private_chat = models.PrivateChat.objects.filter(
        participants=participants[0]
    )

    for participant in participants[1:]:
        existing_private_chat = existing_private_chat.filter(participants=participant)

    if existing_private_chat.exists():
        return True

    return False
